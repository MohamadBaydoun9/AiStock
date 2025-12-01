# Fine-Tuning Documentation (`fine_tune.py`)

**Role:** Accuracy Improvement.

This script is used when adding **more images** to an **existing breed**. Unlike `add_breed.py`, it does not change the model architecture (number of classes remains the same).

## Process

1.  **Load Model**: Loads the existing `pet_classifier.keras`.
2.  **Verify Classes**: Checks if the number of classes in the dataset matches the model's output. If they differ, it redirects to `add_breed.py`.
3.  **Low Learning Rate**: Compiles the model with a very low learning rate (`1e-5`) to carefully adjust weights without forgetting previous knowledge.
4.  **Train**: Runs for a few epochs (default: 2) to incorporate the new data.
5.  **Save**: Updates the model file.

## Usage
Triggered by the backend when uploading images for a breed that already exists in the system.
