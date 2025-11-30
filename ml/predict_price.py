"""
Price Prediction Module (Metadata Only)
Reusable module for predicting pet prices based on metadata
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import joblib
import config

class PricePredictorSingleton:
    """Singleton pattern to load model once"""
    _instance = None
    _model = None
    _encoders = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_model(self):
        """Load model if not already loaded"""
        if self._model is None:
            print(f"Loading price model from {config.PRICE_MODEL_PATH}...")
            self._model = tf.keras.models.load_model(config.PRICE_MODEL_PATH)
            print("✓ Price model loaded")
        return self._model
    
    def get_encoders(self):
        """Load encoders if not already loaded"""
        if self._encoders is None:
            print(f"Loading encoders from {config.PRICE_ENCODERS_PATH}...")
            self._encoders = joblib.load(config.PRICE_ENCODERS_PATH)
            print("✓ Encoders loaded")
        return self._encoders

def predict_price(image_array=None, pet_type='Dog', breed='Unknown', age_months=12, weight_kg=10, health_status=1, vaccinated=1, country='USA'):
    """
    Predict price for a pet (Metadata Only)
    
    Args:
        image_array: Ignored (kept for compatibility)
        pet_type: 'Dog' or 'Cat'
        breed: Breed name (e.g., 'Golden Retriever', 'Persian')
        age_months: Age in months (2-60)
        weight_kg: Weight in kg
        health_status: 0 (normal), 1 (good), 2 (excellent)
        vaccinated: 0 (no) or 1 (yes)
        country: Country of origin (e.g., 'USA', 'Iran', 'Thailand')
    
    Returns:
        float: Predicted price in $
    """
    # Get singleton instance
    predictor = PricePredictorSingleton()
    model = predictor.get_model()
    encoders = predictor.get_encoders()
    
    type_encoder = encoders['type_encoder']
    breed_encoder = encoders['breed_encoder']
    country_encoder = encoders.get('country_encoder')
    
    # Check if model supports country
    if country_encoder is None:
        raise ValueError(
            "Model does not support country-based predictions. "
            "Please retrain the model with country feature using: python ml/train_price_model.py"
        )
    
    # Encode categorical features
    try:
        type_encoded = type_encoder.transform([pet_type])[0]
    except ValueError:
        print(f"Warning: Unknown pet type '{pet_type}', using first available type")
        type_encoded = 0
    
    try:
        breed_encoded = breed_encoder.transform([breed])[0]
    except ValueError:
        print(f"Warning: Unknown breed '{breed}', using first available breed")
        breed_encoded = 0
    
    # Encode country
    try:
        country_encoded = country_encoder.transform([country])[0]
    except ValueError:
        print(f"Warning: Unknown country '{country}', using USA as fallback")
        country_encoded = country_encoder.transform(['USA'])[0] if 'USA' in country_encoder.classes_ else 0
    
    # Prepare metadata with country (7 features)
    metadata = np.array([[
        type_encoded,
        breed_encoded,
        age_months / 60.0,      # Normalize to 0-1
        weight_kg / 50.0,       # Normalize to 0-1
        health_status / 2.0,    # Normalize to 0-1
        vaccinated,
        country_encoded
    ]], dtype=np.float32)
    
    # Predict (Metadata only)
    prediction = model.predict(metadata, verbose=0)
    price = float(prediction[0][0])
    
    # Ensure price is positive
    price = max(0, price)
    
    return price

def predict_price_from_path(image_path, pet_type, breed, age_months, weight_kg, health_status, vaccinated, country='USA'):
    """
    Convenience function: predict price (image path ignored)
    """
    return predict_price(None, pet_type, breed, age_months, weight_kg, health_status, vaccinated, country)

def predict_price_from_bytes(image_bytes, pet_type, breed, age_months, weight_kg, health_status, vaccinated, country='USA'):
    """
    Convenience function: predict price (image bytes ignored)
    """
    return predict_price(None, pet_type, breed, age_months, weight_kg, health_status, vaccinated, country)

# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 7:
        print("Usage: python predict_price.py <type> <breed> <age_months> <weight_kg> <health_status> <vaccinated> [country]")
        print("Example: python predict_price.py Dog 'Golden Retriever' 4 10 2 1 USA")
        sys.exit(1)
    
    pet_type = sys.argv[1]
    breed = sys.argv[2]
    age_months = int(sys.argv[3])
    weight_kg = float(sys.argv[4])
    health_status = int(sys.argv[5])
    vaccinated = int(sys.argv[6])
    country = sys.argv[7] if len(sys.argv) > 7 else 'USA'
    
    price = predict_price(None, pet_type, breed, age_months, weight_kg, health_status, vaccinated, country)
    
    print(f"\n{'='*60}")
    print(f"Predicted Price: ${price:.2f}")
    print(f"{'='*60}")
