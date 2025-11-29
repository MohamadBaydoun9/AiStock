"""
Prediction module for Pet Breed Classification
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import config
from data_loader import preprocess_image, preprocess_image_from_bytes


class PetClassifier:
    """
    Pet breed classifier with prediction capabilities
    """
    
    def __init__(self, model_path=config.MODEL_PATH):
        """
        Initialize classifier
        
        Args:
            model_path: Path to trained model
        """
        self.model = None
        self.class_names = []
        self.pet_types = {}  # Maps breed to pet type (Dog/Cat)
        
        # Load model if exists
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print(f"Warning: Model not found at {model_path}")
            print("Please train the model first using: python ml/train.py")
    
    def load_model(self, model_path):
        """
        Load trained model and class mapping
        
        Args:
            model_path: Path to model file
        """
        print(f"Loading model from {model_path}...")
        try:
            # Try with safe_mode=False for cross-version compatibility
            self.model = keras.models.load_model(model_path, compile=False, safe_mode=False)
        except Exception as e:
            print(f"Warning: Could not load with safe_mode=False: {e}")
            # Fallback to default loading
            self.model = keras.models.load_model(model_path, compile=False)
        
        # Load class mapping
        mapping_path = os.path.join(config.MODEL_DIR, 'class_mapping.json')
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r') as f:
                mapping = json.load(f)
                self.class_names = mapping['classes']
            
            # Parse pet types from class names
            # Format: "Dog/Golden_Retriever" or similar nested structure
            for class_name in self.class_names:
                parts = class_name.split('/')
                if len(parts) >= 2:
                    pet_type = parts[0]  # Dog or Cat
                    breed = parts[1]  # Breed name
                    self.pet_types[class_name] = {
                        'type': pet_type,
                        'breed': breed.replace('_', ' ')
                    }
                else:
                    # Fallback if structure is different
                    self.pet_types[class_name] = {
                        'type': 'Unknown',
                        'breed': class_name.replace('_', ' ')
                    }
            
            print(f"✓ Model loaded with {len(self.class_names)} classes")
        else:
            print(f"Warning: Class mapping not found at {mapping_path}")
    
    def predict_from_path(self, image_path):
        """
        Predict breed from image file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            dict: Prediction results
        """
        if self.model is None:
            return self._get_stub_response()
        
        # Preprocess image
        img = preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(img, verbose=0)
        
        return self._format_prediction(predictions[0])
    
    def predict_from_bytes(self, image_bytes):
        """
        Predict breed from raw image bytes
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            dict: Prediction results
        """
        if self.model is None:
            return self._get_stub_response()
        
        # Preprocess image
        img = preprocess_image_from_bytes(image_bytes)
        
        # Make prediction
        predictions = self.model.predict(img, verbose=0)
        
        return self._format_prediction(predictions[0])
    
    def _format_prediction(self, predictions):
        """
        Format prediction results
        
        Args:
            predictions: Raw model predictions (probabilities)
            
        Returns:
            dict: Formatted prediction
        """
        # Get top prediction
        top_idx = np.argmax(predictions)
        confidence = float(predictions[top_idx])
        class_name = self.class_names[top_idx]
        
        # Parse pet type and breed
        pet_info = self.pet_types.get(class_name, {
            'type': 'Unknown',
            'breed': class_name.replace('_', ' ')
        })
        
        pet_type = pet_info['type']
        breed = pet_info['breed']
        
        # Get price for breed
        breed_key = breed.replace(' ', '_')
        price = config.BREED_PRICES.get(breed_key, config.DEFAULT_PRICE)
        
        # Get top 3 predictions for additional info
        top_3_indices = np.argsort(predictions)[-3:][::-1]
        top_3_predictions = [
            {
                'breed': self.pet_types.get(self.class_names[idx], {}).get('breed', ''),
                'confidence': float(predictions[idx])
            }
            for idx in top_3_indices
        ]
        
        return {
            'product_type': pet_type,
            'product_name': breed,
            'price_predicted': price,
            'confidence': confidence,
            'top_3_predictions': top_3_predictions,
            'exists': False,  # Placeholder for existing product check
            'existing_product': None
        }
    
    def _get_stub_response(self):
        """
        Return stub response when model is not available
        
        Returns:
            dict: Stub prediction
        """
        return {
            'product_type': 'Dog',
            'product_name': 'Golden Retriever',
            'price_predicted': 1500.0,
            'confidence': 0.0,
            'top_3_predictions': [],
            'exists': False,
            'existing_product': None,
            'note': 'Model not trained yet - using stub response'
        }


# Global classifier instance
_classifier = None

def get_classifier():
    """
    Get or create global classifier instance
    
    Returns:
        PetClassifier: Classifier instance
    """
    global _classifier
    if _classifier is None:
        _classifier = PetClassifier()
    return _classifier


# Test function
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        sys.exit(1)
    
    # Make prediction
    classifier = get_classifier()
    result = classifier.predict_from_path(image_path)
    
    print("\n" + "=" * 50)
    print("Prediction Results")
    print("=" * 50)
    print(f"Pet Type: {result['product_type']}")
    print(f"Breed: {result['product_name']}")
    print(f"Predicted Price: ${result['price_predicted']:.2f}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
    print("\nTop 3 Predictions:")
    for i, pred in enumerate(result['top_3_predictions'], 1):
        print(f"{i}. {pred['breed']}: {pred['confidence']*100:.2f}%")
