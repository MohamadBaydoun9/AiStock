# Models Directory Documentation

The `ml/models` directory stores the serialized (saved) machine learning models and their associated metadata.

## Contents

### 1. `pet_classifier.keras`
- **Type**: TensorFlow/Keras Model (SavedModel format).
- **Architecture**: EfficientNetB0 (Pre-trained on ImageNet) + Custom Classification Head.
- **Input**: `(224, 224, 3)` RGB Image.
- **Output**: Probability distribution across all known breeds (Softmax).
- **Created By**: `ml/train.py` or `ml/add_breed.py`.

### 2. `price_predictor.keras`
- **Type**: TensorFlow/Keras Model.
- **Architecture**: Multi-Layer Perceptron (Dense Neural Network).
- **Input**: 7 Numerical/Encoded Features (Type, Breed, Age, Weight, Health, Vaccinated, Country).
- **Output**: Single continuous value (Predicted Price in USD).
- **Created By**: `ml/train_price_model.py`.

### 3. `class_mapping.json`
- **Purpose**: Maps the model's numerical output indices back to human-readable class names.
- **Structure**:
  ```json
  {
    "classes": ["Cat/Persian", "Dog/Golden_Retriever", ...],
    "num_classes": 45
  }
  ```
- **Usage**: Used by `predict.py` to interpret the softmax output vector.

### 4. `price_encoders.joblib`
- **Purpose**: Stores the Scikit-Learn `LabelEncoder` objects used during training.
- **Usage**: Essential for preprocessing new data during inference. It ensures that "Golden Retriever" is encoded to the same integer (e.g., `12`) as it was during training.
- **Created By**: `ml/train_price_model.py`.

### 5. `training_history.json`
- **Purpose**: Logs the loss and accuracy metrics from the last training session.
- **Usage**: Can be visualized to check for overfitting or convergence issues.
