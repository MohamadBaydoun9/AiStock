# Prediction Documentation (`predict.py`)

**Role:** Inference Engine.

This module loads the trained model and provides an interface for making predictions on new images.

## Key Components

### `PetClassifier` Class
- **Initialization**: Loads the `.keras` model and the `class_mapping.json`.
- **`predict_from_path(image_path)`**: Predicts breed from a local file.
- **`predict_from_bytes(image_bytes)`**: Predicts breed from raw bytes (used by API).
- **`_format_prediction`**:
    - Converts raw softmax probabilities into a structured dictionary.
    - Returns: `product_type`, `product_name` (breed), `confidence`, `price_predicted`, and `top_3_predictions`.
    - **Fallback**: If confidence is low, it might return "Unknown" or handle it gracefully.

### Singleton Pattern (`get_classifier`)
- Ensures the model is loaded only once into memory, even if multiple API requests come in.

## Usage
```bash
python ml/predict.py path/to/image.jpg
```
