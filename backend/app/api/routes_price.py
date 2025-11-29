from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add ml directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
project_root = os.path.dirname(backend_dir)
ml_dir = os.path.join(project_root, 'ml')
if ml_dir not in sys.path:
    sys.path.insert(0, ml_dir)

from predict_price import predict_price_from_bytes

router = APIRouter()

class PricePredictionResponse(BaseModel):
    predicted_price: float
    metadata: dict

@router.post("/predict-price", response_model=PricePredictionResponse)
async def predict_price(
    image: UploadFile = File(...),
    pet_type: str = Form(...),
    breed: str = Form(...),
    age_months: int = Form(...),
    weight_kg: float = Form(...),
    health_status: int = Form(...),
    vaccinated: bool = Form(...),
    country: str = Form('USA')
):
    """
    Predict pet price based on image and metadata
    
    Args:
        image: Pet image file
        pet_type: 'Dog' or 'Cat'
        breed: Breed name (e.g., 'Golden Retriever')
        age_months: Age in months (2-60)
        weight_kg: Weight in kg
        health_status: 0 (normal), 1 (good), 2 (excellent)
        vaccinated: True or False
        country: Country of origin (e.g., 'USA', 'Iran')
    
    Returns:
        PricePredictionResponse with predicted price
    """
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Convert vaccinated to int
        vaccinated_int = 1 if vaccinated else 0
        
        # Predict price
        predicted_price = predict_price_from_bytes(
            image_bytes=image_bytes,
            pet_type=pet_type,
            breed=breed,
            age_months=age_months,
            weight_kg=weight_kg,
            health_status=health_status,
            vaccinated=vaccinated_int,
            country=country
        )
        
        print(f"✅ Price prediction: ${predicted_price:.2f} for {breed} from {country} ({age_months}mo, {weight_kg}kg)")
        
        return PricePredictionResponse(
            predicted_price=round(predicted_price, 2),
            metadata={
                "pet_type": pet_type,
                "breed": breed,
                "age_months": age_months,
                "weight_kg": weight_kg,
                "health_status": health_status,
                "vaccinated": vaccinated,
                "country": country
            }
        )
        
    except Exception as e:
        print(f"❌ Price prediction error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return fallback price based on breed
        fallback_prices = {
            'Golden Retriever': 1500,
            'Labrador': 1200,
            'German Shepherd': 1800,
            'Persian': 800,
            'Siamese': 600,
        }
        
        fallback_price = fallback_prices.get(breed, 1000)
        
        return PricePredictionResponse(
            predicted_price=fallback_price,
            metadata={
                "pet_type": pet_type,
                "breed": breed,
                "age_months": age_months,
                "weight_kg": weight_kg,
                "health_status": health_status,
                "vaccinated": vaccinated,
                "note": "Using fallback price due to prediction error"
            }
        )


@router.post("/classify-and-price", response_model=dict)
async def classify_and_price(
    image: UploadFile = File(...),
    age_months: int = Form(...),
    weight_kg: float = Form(...),
    health_status: int = Form(...),
    vaccinated: bool = Form(...),
    country: str = Form('USA')
):
    """
    Combined endpoint: Classify breed + Predict price
    
    This is useful for the frontend flow where user:
    1. Uploads image
    2. Gets breed classification
    3. Enters metadata
    4. Gets price prediction
    
    Args:
        image: Pet image
        age_months: Age in months
        weight_kg: Weight in kg
        health_status: 0, 1, or 2
        vaccinated: True or False
        
    Returns:
        dict with breed classification and price prediction
    """
    try:
        # Read image
        image_bytes = await image.read()
        
        # First, classify the breed
        # Import breed classifier
        from routes_ml_stub import load_predict_module
        predict_module = load_predict_module()
        classifier = predict_module.get_classifier()
        breed_result = classifier.predict_from_bytes(image_bytes)
        
        # Extract breed and type
        pet_type = breed_result['product_type']
        breed = breed_result['product_name']
        
        # Now predict price
        vaccinated_int = 1 if vaccinated else 0
        predicted_price = predict_price_from_bytes(
            image_bytes=image_bytes,
            pet_type=pet_type,
            breed=breed,
            age_months=age_months,
            weight_kg=weight_kg,
            health_status=health_status,
            vaccinated=vaccinated_int,
            country=country
        )
        
        return {
            "classification": {
                "type": pet_type,
                "breed": breed,
                "confidence": breed_result.get('confidence', 0.0)
            },
            "price_prediction": {
                "predicted_price": round(predicted_price, 2),
                "metadata": {
                    "age_months": age_months,
                    "weight_kg": weight_kg,
                    "health_status": health_status,
                    "vaccinated": vaccinated
                }
            }
        }
        
    except Exception as e:
        print(f"❌ Combined prediction error: {e}")
        import traceback
        traceback.print_exc()
        raise
