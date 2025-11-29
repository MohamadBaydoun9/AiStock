"""
Test script for Price Prediction Model
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
import config
import sys

def load_image(image_path):
    """Load and preprocess image"""
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [config.IMG_SIZE, config.IMG_SIZE])
    return img

def predict_price(image_path, pet_type, breed, age_months, weight, health_status, vaccinated):
    """
    Predict price for a pet
    
    Args:
        image_path: Path to pet image
        pet_type: 'Dog' or 'Cat'
        breed: Breed name (e.g., 'Golden Retriever', 'Persian')
        age_months: Age in months (2-60)
        weight: Weight in kg
        health_status: 0 (normal), 1 (good), 2 (excellent)
        vaccinated: 0 (no) or 1 (yes)
    
    Returns:
        float: Predicted price in $
    """
    # Load model
    model_path = os.path.join(config.MODEL_DIR, 'price_predictor.keras')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train first.")
    
    model = tf.keras.models.load_model(model_path)
    
    # Load encoders
    encoders_path = os.path.join(config.MODEL_DIR, 'price_encoders.joblib')
    encoders = joblib.load(encoders_path)
    type_encoder = encoders['type_encoder']
    breed_encoder = encoders['breed_encoder']
    
    # Load and preprocess image
    img = load_image(image_path)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    
    # Encode categorical features
    type_encoded = type_encoder.transform([pet_type])[0]
    breed_encoded = breed_encoder.transform([breed])[0]
    
    # Prepare metadata
    metadata = np.array([[
        type_encoded,
        breed_encoded,
        age_months / 60.0,  # Normalize
        weight / 50.0,      # Normalize
        health_status / 2.0, # Normalize
        vaccinated
    ]], dtype=np.float32)
    
    # Predict
    prediction = model.predict([img, metadata], verbose=0)
    price = float(prediction[0][0])
    
    return price

def test_random_samples(num_samples=5):
    """Test on random samples from the dataset"""
    # Load dataset
    csv_path = os.path.join(config.DATA_DIR, 'price_training_data.csv')
    df = pd.read_csv(csv_path)
    
    # Sample random rows
    samples = df.sample(n=min(num_samples, len(df)))
    
    print("=" * 80)
    print("Testing Price Prediction Model")
    print("=" * 80)
    
    for idx, row in samples.iterrows():
        print(f"\n{'='*80}")
        print(f"Sample {idx + 1}")
        print(f"{'='*80}")
        print(f"Image: {row['image_path']}")
        print(f"Type: {row['type']}")
        print(f"Breed: {row['breed']}")
        print(f"Age: {row['age_months']} months")
        print(f"Weight: {row['weight']} kg")
        print(f"Health Status: {row['health_status']} (0=normal, 1=good, 2=excellent)")
        print(f"Vaccinated: {'Yes' if row['vaccinated'] else 'No'}")
        print(f"\nActual Price: ${row['price']:.2f}")
        
        try:
            predicted_price = predict_price(
                row['image_path'],
                row['type'],
                row['breed'],
                row['age_months'],
                row['weight'],
                row['health_status'],
                row['vaccinated']
            )
            
            error = abs(predicted_price - row['price'])
            error_pct = (error / row['price']) * 100
            
            print(f"Predicted Price: ${predicted_price:.2f}")
            print(f"Error: ${error:.2f} ({error_pct:.1f}%)")
            
            if error_pct < 10:
                print("✅ Excellent prediction!")
            elif error_pct < 20:
                print("✓ Good prediction")
            else:
                print("⚠️  High error")
                
        except Exception as e:
            print(f"❌ Prediction failed: {e}")

def test_custom_example():
    """Test with a custom example"""
    print("\n" + "=" * 80)
    print("Custom Example Test")
    print("=" * 80)
    
    # Get a sample image path
    csv_path = os.path.join(config.DATA_DIR, 'price_training_data.csv')
    df = pd.read_csv(csv_path)
    sample = df.iloc[0]
    
    print("\nExample: Golden Retriever puppy")
    print("Age: 4 months")
    print("Weight: 10 kg")
    print("Health: Excellent (2)")
    print("Vaccinated: Yes")
    
    try:
        price = predict_price(
            sample['image_path'],  # Use any image path
            'Dog',
            'Golden Retriever',
            age_months=4,
            weight=10.0,
            health_status=2,
            vaccinated=1
        )
        print(f"\n💰 Predicted Price: ${price:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'custom':
        test_custom_example()
    else:
        # Test on random samples from dataset
        test_random_samples(num_samples=5)
        
        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        print("\nTo test with custom data, run:")
        print("  python ml/test_price_model.py custom")
        print("\nOr integrate with the API by creating predict_price endpoint!")
