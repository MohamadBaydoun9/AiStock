from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import sys
import os
import importlib.util

router = APIRouter()

class MLResponse(BaseModel):
    product_type: str
    product_name: str
    price_predicted: float
    confidence: float = 0.0
    exists: bool
    existing_product: Optional[dict] = None

# Load predict module dynamically
def load_predict_module():
    """Dynamically load the predict module and its dependencies from ml/"""
    # Get path to ml directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    project_root = os.path.dirname(backend_dir)
    ml_dir = os.path.join(project_root, 'ml')
    
    print(f"🔍 Loading ML modules from: {ml_dir}")
    
    if not os.path.exists(ml_dir):
        raise FileNotFoundError(f"ml directory not found at {ml_dir}")
    
    # Add ml directory to path so imports work
    if ml_dir not in sys.path:
        sys.path.insert(0, ml_dir)
    
    # Load config module first (required by predict)
    config_path = os.path.join(ml_dir, 'config.py')
    if os.path.exists(config_path):
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        sys.modules["config"] = config_module
        spec.loader.exec_module(config_module)
        print(f"✅ Loaded config module")
    
    # Load data_loader module (required by predict)
    data_loader_path = os.path.join(ml_dir, 'data_loader.py')
    if os.path.exists(data_loader_path):
        spec = importlib.util.spec_from_file_location("data_loader", data_loader_path)
        data_loader_module = importlib.util.module_from_spec(spec)
        sys.modules["data_loader"] = data_loader_module
        spec.loader.exec_module(data_loader_module)
        print(f"✅ Loaded data_loader module")
    
    # Load predict module
    predict_path = os.path.join(ml_dir, 'predict.py')
    if not os.path.exists(predict_path):
        raise FileNotFoundError(f"predict.py not found at {predict_path}")
    
    spec = importlib.util.spec_from_file_location("predict", predict_path)
    predict_module = importlib.util.module_from_spec(spec)
    sys.modules["predict"] = predict_module
    spec.loader.exec_module(predict_module)
    print(f"✅ Loaded predict module")
    
    return predict_module

@router.post("/classify-and-predict", response_model=MLResponse)
async def classify_and_predict(file: UploadFile = File(...)):
    """
    Classify pet image and predict breed using trained TensorFlow model
    Falls back to stub if model not available
    """
    try:
        # Load predict module
        predict_module = load_predict_module()
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Get classifier and make prediction
        classifier = predict_module.get_classifier()
        result = classifier.predict_from_bytes(image_bytes)
        
        print(f"✅ Prediction: {result['product_type']} - {result['product_name']} (confidence: {result.get('confidence', 0):.2f})")
        
        return MLResponse(
            product_type=result['product_type'],
            product_name=result['product_name'],
            price_predicted=result['price_predicted'],
            confidence=result.get('confidence', 0.0),
            exists=False,
            existing_product=None
        )
    except Exception as e:
        # Log the actual error for debugging
        print(f"❌ Model prediction error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Fallback to stub
        return MLResponse(
            product_type="Dog",
            product_name="Golden Retriever",
            price_predicted=1500.0,
            confidence=0.0,
            exists=False,
            existing_product=None
        )
