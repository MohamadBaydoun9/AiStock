"""
Script to add a NEW breed class to an existing trained model.
Performs 'Model Surgery' to expand the output layer and transfer weights.
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import numpy as np
import config
from data_loader import create_data_generators, get_class_weights
from model import create_model, get_callbacks
import json
import sys

# Force UTF-8 for Windows consoles/logs
sys.stdout.reconfigure(encoding='utf-8')

def add_new_breed_to_model():
    print("=" * 50)
    print("Model Surgery: Adding New Breed")
    print("=" * 50)

    # 1. Verify paths
    if not os.path.exists(config.MODEL_PATH):
        print("Error: No existing model found to update.")
        return False

    # 2. Load Data & Detect New Classes
    print("\nScanning dataset for new breeds...")
    train_gen, val_gen, class_names = create_data_generators()
    new_num_classes = len(class_names)
    
    # 3. Load Old Class Mapping
    mapping_path = os.path.join(config.MODEL_DIR, 'class_mapping.json')
    if os.path.exists(mapping_path):
        with open(mapping_path, 'r') as f:
            old_mapping = json.load(f)
            old_num_classes = old_mapping['num_classes']
            old_class_names = old_mapping['classes']
    else:
        print("Warning: No class mapping found. Assuming this is a fresh train.")
        old_num_classes = 0
        old_class_names = []

    print(f"\nStats:")
    print(f"   Old Class Count: {old_num_classes}")
    print(f"   New Class Count: {new_num_classes}")

    if new_num_classes <= old_num_classes:
        print("\nWarning: No new classes detected. Use 'fine_tune.py' instead for existing breeds.")
        return False

    # 4. Load Old Model
    print("\nLoading old model...")
    old_model = keras.models.load_model(config.MODEL_PATH)
    
    # 5. Create New Model Architecture
    print(f"\nConstructing new model with {new_num_classes} outputs...")
    # We create a fresh model architecture with the NEW number of classes
    new_model, base_model = create_model(new_num_classes)

    # 6. Transfer Weights (The "Surgery")
    print("\nPerforming weight transfer...")
    
    # Transfer weights for all layers EXCEPT the final classification layer
    # The final layer is usually named 'dense_1' or similar, but let's be safe and index from end
    # In our create_model, the last layer is the output Dense layer
    
    for i in range(len(old_model.layers) - 1):
        new_model.layers[i].set_weights(old_model.layers[i].get_weights())
        
    # Now handle the final layer
    old_last_layer = old_model.layers[-1]
    new_last_layer = new_model.layers[-1]
    
    old_weights, old_biases = old_last_layer.get_weights()
    
    # Initialize new weights (randomly or with zeros)
    # Shape is (input_dim, num_classes)
    input_dim = old_weights.shape[0]
    new_weights = np.random.normal(0, 0.01, (input_dim, new_num_classes))
    new_biases = np.zeros((new_num_classes,))
    
    # Copy over the old weights to the corresponding indices
    # We need to match class names to ensure consistency
    print("   Mapping old weights to new indices...")
    
    # Create index maps
    new_class_to_idx = {name: i for i, name in enumerate(class_names)}
    
    matched_count = 0
    for i, old_name in enumerate(old_class_names):
        if old_name in new_class_to_idx:
            new_idx = new_class_to_idx[old_name]
            # Copy weights and bias for this class
            new_weights[:, new_idx] = old_weights[:, i]
            new_biases[new_idx] = old_biases[i]
            matched_count += 1
            
    print(f"   Transferred weights for {matched_count} existing classes")
    
    # Set the weights into the new layer
    new_last_layer.set_weights([new_weights, new_biases])
    
    print("Surgery complete. Model expanded.")

    # 7. Compile
    new_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-4), # Lower rate for stability
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )

    # 8. Train (Fine-tune)
    print("\n" + "=" * 50)
    print("Phase 1: Training New Breed Connections")
    print("=" * 50)
    
    class_weights = get_class_weights(train_gen)
    callbacks = get_callbacks()
    
    # Train for a few epochs to settle the new weights
    history = new_model.fit(
        train_gen,
        epochs=1, # Enough to learn the new class
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    # 9. Save Everything
    print("\nSaving updated model...")
    new_model.save(config.MODEL_PATH)
    
    # Update mapping
    new_mapping = {
        'classes': class_names,
        'num_classes': new_num_classes
    }
    with open(mapping_path, 'w') as f:
        json.dump(new_mapping, f, indent=2)
        
    print("\nSUCCESS: New breed added and model updated!")
    return True

if __name__ == '__main__':
    # GPU Setup
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
            
    add_new_breed_to_model()
