
import os
import tensorflow as tf
import numpy as np
import config
from data_loader import create_data_generators
from PIL import Image

def debug_data():
    print("Debugging data loader...")
    
    train_ds, val_ds, class_names = create_data_generators()
    
    print(f"Classes: {class_names}")
    
    # Get one batch
    for images, labels in train_ds.take(1):
        print(f"Batch shape: {images.shape}")
        print(f"Labels shape: {labels.shape}")
        
        # Check value range
        print(f"Min pixel value: {np.min(images)}")
        print(f"Max pixel value: {np.max(images)}")
        
        # Save first 5 images
        for i in range(min(5, len(images))):
            img = images[i].numpy()
            # Convert back to 0-255 for saving
            img_save = (img * 255).astype(np.uint8)
            
            label_idx = np.argmax(labels[i])
            label_name = class_names[label_idx]
            
            filename = f"debug_img_{i}_{label_name.replace('/', '_')}.jpg"
            Image.fromarray(img_save).save(filename)
            print(f"Saved {filename} (Label: {label_name})")
            
        break

if __name__ == '__main__':
    debug_data()
