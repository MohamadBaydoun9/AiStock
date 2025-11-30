"""
Training script for Price Prediction Model (Metadata Only)
Architecture: Metadata Features → Dense Layers → Price
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import config
import joblib

# GPU Configuration
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU Detected: {len(gpus)} device(s)")
    except RuntimeError as e:
        print(f"GPU setup error: {e}")
else:
    print("⚠️  No GPU detected - training will use CPU")

def load_and_prepare_data():
    """Load CSV and prepare features"""
    print("\n📁 Loading dataset...")
    csv_path = os.path.join(config.DATA_DIR, 'price_training_data.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}.\n"
            "Please run: python ml/generate_price_dataset.py"
        )
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} samples")
    
    # Encode categorical features
    type_encoder = LabelEncoder()
    breed_encoder = LabelEncoder()
    country_encoder = LabelEncoder()
    
    df['type_encoded'] = type_encoder.fit_transform(df['type'])
    df['breed_encoded'] = breed_encoder.fit_transform(df['breed'])
    df['country_encoded'] = country_encoder.fit_transform(df['country'])
    
    print(f"\nTypes: {list(type_encoder.classes_)}")
    print(f"Breeds: {list(breed_encoder.classes_)}")
    print(f"Countries: {list(country_encoder.classes_)}")
    
    return df, type_encoder, breed_encoder, country_encoder

def create_price_prediction_model(num_types, num_breeds):
    """
    Create metadata-only price prediction model
    
    Architecture:
    - Metadata Input (7 features)
    - Dense Layers with BatchNormalization and Dropout
    - Output: Price
    """
    # Metadata input
    # 7 features: type_encoded, breed_encoded, age_months, weight, health_status, vaccinated, country_encoded
    metadata_input = layers.Input(shape=(7,), name='metadata_input')  
    
    # Dense network
    x = layers.Dense(128, activation='relu')(metadata_input)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    x = layers.Dense(64, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    
    x = layers.Dense(32, activation='relu')(x)
    
    # Output: price (continuous value)
    price_output = layers.Dense(1, activation='linear', name='price_output')(x)
    
    # Create model
    model = models.Model(
        inputs=metadata_input,
        outputs=price_output,
        name='price_predictor_metadata'
    )
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='mae',  # Mean Absolute Error
        metrics=['mae', 'mse', keras.metrics.RootMeanSquaredError(name='rmse')]
    )
    
    return model

def create_dataset(df, batch_size=32, shuffle=True):
    """Create tf.data.Dataset for training (Metadata Only)"""
    
    # Convert dataframe to numpy arrays for efficiency
    # Features: [type, breed, age, weight, health, vaccinated, country]
    # We normalize continuous variables here
    
    features = np.stack([
        df['type_encoded'].values,
        df['breed_encoded'].values,
        df['age_months'].values / 60.0,  # Normalize age (0-5 years)
        df['weight'].values / 50.0,      # Normalize weight (approx max 50kg)
        df['health_status'].values / 2.0, # Normalize health (0-2)
        df['vaccinated'].values,
        df['country_encoded'].values
    ], axis=1).astype(np.float32)
    
    targets = df['price'].values.astype(np.float32)
    
    dataset = tf.data.Dataset.from_tensor_slices((features, targets))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(df), seed=42)
    
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    return dataset

def train():
    """Main training function"""
    print("=" * 60)
    print("Price Prediction Model (Metadata Only) - Training")
    print("=" * 60)
    
    # Load data
    df, type_encoder, breed_encoder, country_encoder = load_and_prepare_data()
    
    # Split data
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    print(f"\nSplit: {len(train_df)} train, {len(val_df)} validation")
    
    # Create datasets
    print("\n📦 Creating datasets...")
    train_ds = create_dataset(train_df, batch_size=32, shuffle=True)
    val_ds = create_dataset(val_df, batch_size=32, shuffle=False)
    
    # Create model
    print("\n🏗️  Building model...")
    num_types = len(type_encoder.classes_)
    num_breeds = len(breed_encoder.classes_)
    model = create_price_prediction_model(num_types, num_breeds)
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            os.path.join(config.MODEL_DIR, 'price_predictor.keras'),
            monitor='val_mae',
            save_best_only=True,
            mode='min',
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_mae',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # Train
    print("\n" + "=" * 60)
    print("Training...")
    print("=" * 60)
    
    history = model.fit(
        train_ds,
        epochs=50,
        validation_data=val_ds,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    print("\n" + "=" * 60)
    print("Final Evaluation")
    print("=" * 60)
    
    results = model.evaluate(val_ds, verbose=1)
    print(f"\n✓ Validation MAE: ${results[1]:.2f}")
    print(f"✓ Validation RMSE: ${results[3]:.2f}")
    
    # Save encoders
    encoders_path = os.path.join(config.MODEL_DIR, 'price_encoders.joblib')
    joblib.dump({
        'type_encoder': type_encoder,
        'breed_encoder': breed_encoder,
        'country_encoder': country_encoder
    }, encoders_path)
    print(f"\n✅ Encoders saved to {encoders_path}")
    
    print("\n" + "=" * 60)
    print("Training Complete! 🎉")
    print("=" * 60)
    print(f"\nModel saved to: {os.path.join(config.MODEL_DIR, 'price_predictor.keras')}")
    print("\nYou can now use the model for predictions!")

if __name__ == '__main__':
    # Set random seeds
    import random
    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)
    
    train()
