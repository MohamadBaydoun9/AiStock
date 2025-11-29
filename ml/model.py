"""
Pet Breed Classification Model using MobileNetV3
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV3Small
import config


def create_model(num_classes):
    """
    Create EfficientNetB0 based model for pet breed classification
    
    Justification for EfficientNetB0:
    1. Higher Accuracy: Better than MobileNetV3 for fine-grained classification
    2. Efficient: Good trade-off between speed and accuracy
    3. Built-in Preprocessing: Handles normalization internally
    
    Args:
        num_classes: Number of breed classes to predict
        
    Returns:
        keras.Model: Compiled model
    """
    
    # Input layer (expecting [0, 255] pixel values)
    inputs = keras.Input(shape=(config.IMG_SIZE, config.IMG_SIZE, 3))
    
    # Data augmentation layers (active only during training)
    x = layers.RandomFlip("horizontal")(inputs)
    x = layers.RandomRotation(0.2)(x)
    x = layers.RandomZoom(0.2)(x)
    x = layers.RandomContrast(0.2)(x)
    x = layers.RandomBrightness(0.2)(x)
    
    # Load pre-trained EfficientNetB0
    # Note: EfficientNet expects [0, 255] inputs
    base_model = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_tensor=x,
        pooling='avg'
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Get output from base model
    # Note: We use the output of base_model directly since we passed 'x' as input_tensor
    # However, standard Keras usage often separates them. Let's do it the standard functional way
    # to avoid confusion with input_tensor.
    
    # Re-instantiate without input_tensor to be cleaner
    base_model = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_shape=(config.IMG_SIZE, config.IMG_SIZE, 3),
        pooling='avg'
    )
    base_model.trainable = False
    
    x = base_model(x, training=False)
    
    # Custom classification head
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(512, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    # Create model
    model = models.Model(inputs, outputs, name='pet_breed_classifier_effnet')
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model, base_model


def unfreeze_and_fine_tune(model, base_model, num_classes):
    """
    Unfreeze base model and fine-tune with lower learning rate
    
    Args:
        model: Compiled model
        base_model: Base MobileNetV3 model
        num_classes: Number of classes
        
    Returns:
        keras.Model: Model ready for fine-tuning
    """
    # Unfreeze base model
    base_model.trainable = True
    
    # Fine-tune only the last layers (freeze first layers)
    # This preserves low-level features learned on ImageNet
    for layer in base_model.layers[:-30]:  # Freeze all but last 30 layers
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=config.FINE_TUNE_LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(f"Fine-tuning model with {sum([1 for layer in model.layers if layer.trainable])} trainable layers")
    
    return model


def get_callbacks():
    """
    Create training callbacks
    
    Returns:
        list: List of Keras callbacks
    """
    callbacks = [
        # Save best model
        keras.callbacks.ModelCheckpoint(
            config.MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=config.REDUCE_LR_PATIENCE,
            min_lr=1e-7,
            verbose=1
        ),
        
        # TensorBoard logging
        keras.callbacks.TensorBoard(
            log_dir='logs',
            histogram_freq=1
        )
    ]
    
    return callbacks
