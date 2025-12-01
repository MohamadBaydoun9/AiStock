# Config Documentation (`config.py`)

**Role:** Central Configuration Hub.

This file defines all hyperparameters, file paths, and constants used across the machine learning pipeline. Changing values here propagates to all training and prediction scripts.

## Key Configurations

### 1. Paths
- Defines absolute paths for `DATA_DIR`, `TRAIN_DIR`, `VAL_DIR`, and `MODEL_DIR`.
- Ensures cross-platform compatibility using `os.path.join`.

### 2. Model Hyperparameters
- **`IMG_SIZE = 224`**: Input resolution for EfficientNetB0.
- **`BATCH_SIZE = 32`**: Number of images processed per step.
- **`EPOCHS = 50`**: Maximum training iterations.
- **`LEARNING_RATE = 0.001`**: Initial step size for the optimizer.

### 3. Data Augmentation
- Defines parameters for random transformations (Rotation, Zoom, Brightness) to increase dataset diversity and prevent overfitting.

### 4. Breed Prices
- **`BREED_PRICES`**: A dictionary mapping breed names to default market prices.
- **Usage**: Used as a fallback or baseline for the price prediction system when the ML model is uncertain or for generating synthetic data.

## System Flow
Imported by almost every other script (`train.py`, `predict.py`, `data_loader.py`) to ensure consistency.
