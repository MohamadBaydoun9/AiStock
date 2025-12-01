# Model Architecture Documentation (`model.py`)

**Role:** Neural Network Definition.

This file contains the factory functions to build and compile the TensorFlow/Keras models.

## Key Functions

### 1. `create_model(num_classes)`
- **Base Model**: **EfficientNetB0** (pre-trained on ImageNet).
    - *Why?* It offers a superior accuracy-to-efficiency ratio compared to older models like ResNet50 or VGG16.
- **Transfer Learning**:
    - The base model is initially **frozen** (`trainable=False`) to preserve its learned feature extractors.
- **Custom Head**:
    - Adds a `GlobalAveragePooling2D` layer to reduce spatial dimensions.
    - Adds `BatchNormalization` and `Dropout` (0.4) for regularization.
    - Adds a `Dense` hidden layer (512 units) with L2 regularization.
    - **Output Layer**: `Dense(num_classes, activation='softmax')`.

### 2. `unfreeze_and_fine_tune(model, base_model, num_classes)`
- **Purpose**: Unlocks the deeper layers of EfficientNet to adapt them specifically to pet features.
- **Strategy**:
    - Unfreezes the top 30 layers of the base model.
    - Recompiles the model with a very low learning rate (`1e-5`) to avoid destroying the pre-trained weights.

### 3. `get_callbacks()`
- Returns a list of Keras callbacks:
    - **ModelCheckpoint**: Saves the best model based on validation accuracy.
    - **EarlyStopping**: Stops training if validation loss stops improving.
    - **ReduceLROnPlateau**: Lowers learning rate when progress stalls.
    - **TensorBoard**: Logs metrics for visualization.
