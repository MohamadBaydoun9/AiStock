"""
Configuration for Pet Breed Classification Model
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'val')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'pet_classifier.keras')
PRICE_MODEL_PATH = os.path.join(MODEL_DIR, 'price_predictor.keras')
PRICE_ENCODERS_PATH = os.path.join(MODEL_DIR, 'price_encoders.joblib')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Model hyperparameters
IMG_SIZE = 224  # MobileNetV3 input size (reduce to 160 for 2x speed)
BATCH_SIZE = 32  # Increase to 64 or 128 if you have enough RAM/GPU memory
EPOCHS = 50  # Increased for EfficientNet
LEARNING_RATE = 0.001
FINE_TUNE_LEARNING_RATE = 0.0001
FINE_TUNE_EPOCHS = 10  # Reduced from 20 for faster training

# Quick training mode (uncomment to use)
# IMG_SIZE = 160  # Smaller images = faster
# BATCH_SIZE = 64  # Larger batches = faster (if memory allows)
# EPOCHS = 20  # Fewer epochs
# FINE_TUNE_EPOCHS = 5  # Minimal fine-tuning

# Data augmentation parameters
ROTATION_RANGE = 15
ZOOM_RANGE = 0.1
BRIGHTNESS_RANGE = (0.8, 1.2)
HORIZONTAL_FLIP = True

# Training parameters
VALIDATION_SPLIT = 0.2
EARLY_STOPPING_PATIENCE = 5
REDUCE_LR_PATIENCE = 3

# Pet type categories (top level)
PET_TYPES = ['Dog', 'Cat']

# Average prices per breed (you can customize this)
BREED_PRICES = {
    # Dogs
    'Golden_Retriever': 1500.0,
    'Labrador': 1200.0,
    'German_Shepherd': 1800.0,
    'Bulldog': 2000.0,
    'Poodle': 1600.0,
    'Beagle': 1000.0,
    'Husky': 1700.0,
    'Corgi': 1400.0,
    
    # Cats
    'Persian': 800.0,
    'Siamese': 600.0,
    'Maine_Coon': 900.0,
    'Bengal': 1200.0,
    'Ragdoll': 850.0,
    'British_Shorthair': 700.0,
    'Sphynx': 1500.0,
    'Scottish_Fold': 1000.0,
}

# Default price if breed not found
DEFAULT_PRICE = 500.0
