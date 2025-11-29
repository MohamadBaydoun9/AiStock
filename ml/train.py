"""
Training script for Pet Breed Classification Model
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging

import tensorflow as tf
from tensorflow import keras

# GPU Configuration - Enable memory growth for RTX 5070
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Enable memory growth (prevents TF from allocating all 8GB VRAM at once)
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU Detected: {len(gpus)} device(s)")
        print(f"   GPU will be used for training (10-20x speedup!)")
    except RuntimeError as e:
        print(f"GPU setup error: {e}")
else:
    print("⚠️  No GPU detected - training will use CPU (slower)")

import config
from data_loader import create_data_generators, get_class_weights
from model import create_model, unfreeze_and_fine_tune, get_callbacks
import json


def train():
    """
    Main training function
    """
    print("=" * 50)
    print("Pet Breed Classification - Training")
    print("=" * 50)
    
    # Check if data directories exist
    if not os.path.exists(config.TRAIN_DIR) or not os.listdir(config.TRAIN_DIR):
        print(f"ERROR: Training data not found in {config.TRAIN_DIR}")
        print("\nPlease organize your data as follows:")
        print("ml/data/train/")
        print("  ├── Dog/")
        print("  │   ├── Golden_Retriever/")
        print("  │   │   ├── img1.jpg")
        print("  │   │   └── ...")
        print("  │   └── Labrador/")
        print("  └── Cat/")
        print("      ├── Persian/")
        print("      └── Siamese/")
        return
    
    if not os.path.exists(config.VAL_DIR) or not os.listdir(config.VAL_DIR):
        print(f"ERROR: Validation data not found in {config.VAL_DIR}")
        print("Please create a validation set with the same structure as training data")
        return
    
    # Create data generators
    print("\n📁 Loading data...")
    train_gen, val_gen, class_names = create_data_generators()
    
    # Get number of classes
    num_classes = len(class_names)
    print(f"\n✓ Detected {num_classes} classes (breeds)")
    
    # Calculate class weights for imbalanced data
    class_weights = get_class_weights(train_gen)
    
    # Save class names for inference
    class_mapping = {
        'classes': class_names,
        'num_classes': num_classes
    }
    with open(os.path.join(config.MODEL_DIR, 'class_mapping.json'), 'w') as f:
        json.dump(class_mapping, f, indent=2)
    print(f"✓ Saved class mapping to {config.MODEL_DIR}/class_mapping.json")
    
    # Create model
    print("\n🏗️  Building model...")
    model, base_model = create_model(num_classes)
    model.summary()
    
    # Get callbacks
    callbacks = get_callbacks()
    
    # Phase 1: Train only classification head
    print("\n" + "=" * 50)
    print("Phase 1: Training Classification Head")
    print("=" * 50)
    
    history = model.fit(
        train_gen,
        epochs=config.EPOCHS,
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune entire model
    print("\n" + "=" * 50)
    print("Phase 2: Fine-Tuning Full Model")
    print("=" * 50)
    
    model = unfreeze_and_fine_tune(model, base_model, num_classes)
    
    history_fine = model.fit(
        train_gen,
        epochs=config.FINE_TUNE_EPOCHS,
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=callbacks,
        initial_epoch=len(history.history['loss']),
        verbose=1
    )
    
    # Evaluate final model
    print("\n" + "=" * 50)
    print("Final Evaluation")
    print("=" * 50)
    
    results = model.evaluate(val_gen, verbose=1)
    print(f"\n✓ Final Validation Accuracy: {results[1]:.4f}")
    print(f"✓ Final Validation Top-3 Accuracy: {results[2]:.4f}")
    
    # Save final model
    model.save(config.MODEL_PATH)
    print(f"\n✅ Model saved to {config.MODEL_PATH}")
    
    # Save training history
    history_dict = {
        'phase1': {k: [float(v) for v in vals] for k, vals in history.history.items()},
        'phase2': {k: [float(v) for v in vals] for k, vals in history_fine.history.items()}
    }
    with open(os.path.join(config.MODEL_DIR, 'training_history.json'), 'w') as f:
        json.dump(history_dict, f, indent=2)
    print(f"✓ Training history saved to {config.MODEL_DIR}/training_history.json")
    
    print("\n" + "=" * 50)
    print("Training Complete! 🎉")
    print("=" * 50)
    print(f"\nYour model is ready to use at: {config.MODEL_PATH}")
    print("You can now restart the backend to use the trained model for predictions.")


if __name__ == '__main__':
    # Set random seeds for reproducibility
    import numpy as np
    import random
    
    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)
    
    # Run training
    train()
