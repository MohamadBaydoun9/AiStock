# Price Model Training Documentation (`train_price_model.py`)

**Role:** Price Model Training.

This script trains the metadata-based price predictor using the synthetic dataset.

## Process

1.  **Load Data**: Reads `ml/data/price_training_data.csv`.
2.  **Encoding**:
    - Fits `LabelEncoder` for Type, Breed, and Country.
    - Saves these encoders to `ml/models/price_encoders.joblib` for use during prediction.
3.  **Normalization**: Scales continuous variables (Age, Weight, Health) to a `0-1` range.
4.  **Model Architecture**:
    - Input: 7 features.
    - Hidden Layers: Dense(128) -> Dense(64) -> Dense(32) with BatchNormalization and Dropout.
    - Output: Dense(1) (Linear activation).
5.  **Training**: Optimizes for Mean Absolute Error (MAE).
6.  **Save**: Saves the trained model to `ml/models/price_predictor.keras`.

## Usage
```bash
python ml/train_price_model.py
```
