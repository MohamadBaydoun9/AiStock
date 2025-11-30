"""
Fine-tuning script for adding more training data to an existing model
Use this when you want to add more images for specific breeds without starting from scratch
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras

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

import config
from data_loader import create_data_generators, get_class_weights
from model import get_callbacks
import json

def fine_tune_existing_model():
    """
    Fine-tune an existing trained model with additional data
    """
    print("=" * 50)
    print("Pet Breed Classification - Fine-Tuning")
    print("=" * 50)
    
    # Check if existing model exists
    if not os.path.exists(config.MODEL_PATH):
        print(f"❌ ERROR: No existing model found at {config.MODEL_PATH}")
        print("Please train the initial model first using train.py")
        return
    
    print(f"\n✓ Found existing model at {config.MODEL_PATH}")
    
    # Load existing model
    print("\n📦 Loading existing model...")
    model = keras.models.load_model(config.MODEL_PATH)
    print("✓ Model loaded successfully")
    
    # Create data generators with new data
    print("\n📁 Loading training data (including new images)...")
    train_gen, val_gen, class_names = create_data_generators()
    
    num_classes = len(class_names)
    print(f"\n✓ Detected {num_classes} classes (breeds)")
    
    # Calculate class weights
    class_weights = get_class_weights(train_gen)
    
    # Update class mapping
    class_mapping = {
        'classes': class_names,
        'num_classes': num_classes
    }
    with open(os.path.join(config.MODEL_DIR, 'class_mapping.json'), 'w') as f:
        json.dump(class_mapping, f, indent=2)
    
    # Configure for fine-tuning with lower learning rate
    print("\n🔧 Configuring model for fine-tuning...")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.00001),  # Very low learning rate
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    # Get callbacks
    callbacks = get_callbacks()
    
    # Fine-tune with new data
    print("\n" + "=" * 50)
    print("Fine-Tuning with Additional Data")
    print("=" * 50)
    print("This will improve the model's accuracy on Akita Inu vs Shiba Inu")
    
    # Use fewer epochs for fine-tuning
    fine_tune_epochs = 10
    
    history = model.fit(
        train_gen,
        epochs=fine_tune_epochs,
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    print("\n" + "=" * 50)
    print("Final Evaluation")
    print("=" * 50)
    
    results = model.evaluate(val_gen, verbose=1)
    print(f"\n✓ Validation Accuracy: {results[1]:.4f}")
    print(f"✓ Validation Top-3 Accuracy: {results[2]:.4f}")
    
    # Save fine-tuned model
    model.save(config.MODEL_PATH)
    print(f"\n✅ Fine-tuned model saved to {config.MODEL_PATH}")
    
    # Save training history
    history_dict = {
        'fine_tuning': {k: [float(v) for v in vals] for k, vals in history.history.items()}
    }
    with open(os.path.join(config.MODEL_DIR, 'fine_tuning_history.json'), 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print("\n" + "=" * 50)
    print("Fine-Tuning Complete! 🎉")
    print("=" * 50)
    print(f"\nYour improved model is ready at: {config.MODEL_PATH}")
    print("Restart the backend to use the updated model.")


if __name__ == '__main__':
    import numpy as np
    import random
    
    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)
    
    fine_tune_existing_model()
