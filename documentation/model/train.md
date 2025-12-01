# Training Script Documentation (`train.py`)

**Role:** Main Training Pipeline.

This script orchestrates the entire training process for the Pet Breed Classifier.

## System Flow

1.  **GPU Setup**: Detects available GPUs and enables memory growth to prevent OOM errors.
2.  **Data Loading**: Calls `create_data_generators()` to load train/val datasets.
3.  **Model Building**: Initializes the EfficientNetB0 architecture.
4.  **Phase 1 (Head Training)**:
    - Trains only the top custom layers for `EPOCHS` (default: 50).
    - The base EfficientNet is frozen.
5.  **Phase 2 (Fine-Tuning)**:
    - Unfreezes the top 30 layers of EfficientNet.
    - Trains for `FINE_TUNE_EPOCHS` (default: 10) with a lower learning rate.
6.  **Evaluation**: Calculates final accuracy on the validation set.
7.  **Saving**:
    - Saves the model to `ml/models/pet_classifier.keras`.
    - Saves the class mapping to `ml/models/class_mapping.json`.
    - Saves training history to `ml/models/training_history.json`.

## Usage
```bash
python ml/train.py
```
