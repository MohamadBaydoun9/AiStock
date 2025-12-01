# Price Prediction Documentation (`predict_price.py`)

**Role:** Metadata-based Price Inference.

This module predicts the market price of a pet based on structured metadata, independent of the image visual features.

## Key Components

### `PricePredictorSingleton`
- **Efficiency**: Loads the price prediction model (`price_predictor.keras`) and encoders (`price_encoders.joblib`) only once.

### `predict_price(...)`
- **Inputs**: `pet_type`, `breed`, `age_months`, `weight_kg`, `health_status`, `vaccinated`, `country`.
- **Preprocessing**:
    - Uses loaded `LabelEncoders` to convert categorical strings (Breed, Country) into integers.
    - Normalizes numerical inputs (e.g., divides age by 60, weight by 50) to match the training scale.
- **Inference**: Runs the inputs through the Dense Neural Network.
- **Output**: Returns a float value (USD).

## Usage
Used by the backend's `/ml/predict-price` endpoint.
