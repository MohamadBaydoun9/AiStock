"""
Data Loading and Augmentation for Pet Breed Classification
"""
import tensorflow as tf
import os
import numpy as np
import config

def load_dataset_from_directory(directory, batch_size=config.BATCH_SIZE, img_size=config.IMG_SIZE, shuffle=True, seed=42):
    """
    Load dataset from directory with nested structure (Type/Breed)
    
    Args:
        directory: Path to data directory
        batch_size: Batch size
        img_size: Target image size
        shuffle: Whether to shuffle data
        seed: Random seed
        
    Returns:
        tuple: (dataset, class_names, file_paths, labels)
    """
    file_paths = []
    labels = []
    class_names = []
    
    # 1. Scan directory to find classes and files
    # Structure: directory/Type/Breed/image.jpg
    print(f"Scanning {directory}...")
    
    # First pass: find all classes
    classes_set = set()
    for pet_type in os.listdir(directory):
        pet_type_dir = os.path.join(directory, pet_type)
        if os.path.isdir(pet_type_dir):
            for breed in os.listdir(pet_type_dir):
                breed_dir = os.path.join(pet_type_dir, breed)
                if os.path.isdir(breed_dir):
                    class_path = f"{pet_type}/{breed}"
                    classes_set.add(class_path)
    
    class_names = sorted(list(classes_set))
    class_to_index = {cls: i for i, cls in enumerate(class_names)}
    
    if not class_names:
        print("Warning: No nested classes found. Checking top-level...")
        # Fallback for flat structure
        for cls in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, cls)):
                classes_set.add(cls)
        class_names = sorted(list(classes_set))
        class_to_index = {cls: i for i, cls in enumerate(class_names)}

    print(f"Found {len(class_names)} classes: {class_names}")

    # Second pass: collect files
    for pet_type in os.listdir(directory):
        pet_type_dir = os.path.join(directory, pet_type)
        if os.path.isdir(pet_type_dir):
            # Check if this is a class itself or a container
            if pet_type in class_to_index:
                 # Flat structure case
                 cls_idx = class_to_index[pet_type]
                 for fname in os.listdir(pet_type_dir):
                    if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_paths.append(os.path.join(pet_type_dir, fname))
                        labels.append(cls_idx)
            else:
                # Nested structure case
                for breed in os.listdir(pet_type_dir):
                    breed_dir = os.path.join(pet_type_dir, breed)
                    if os.path.isdir(breed_dir):
                        class_path = f"{pet_type}/{breed}"
                        if class_path in class_to_index:
                            cls_idx = class_to_index[class_path]
                            for fname in os.listdir(breed_dir):
                                if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                                    file_paths.append(os.path.join(breed_dir, fname))
                                    labels.append(cls_idx)
    
    print(f"Found {len(file_paths)} images")
    
    if not file_paths:
        raise ValueError(f"No images found in {directory}")

    # 2. Create dataset
    # Convert to one-hot encoding
    labels = tf.keras.utils.to_categorical(labels, num_classes=len(class_names))
    
    dataset = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    
    # 3. Map function to load images
    def process_path(file_path, label):
        # Load image
        img = tf.io.read_file(file_path)
        img = tf.io.decode_image(img, channels=3, expand_animations=False)
        img.set_shape([None, None, 3])  # Explicitly set shape for TensorFlow graph
        img = tf.image.resize(img, [img_size, img_size])
        # EfficientNet expects [0, 255] inputs, so we don't normalize here
        return img, label

    dataset = dataset.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000, seed=seed)
    
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    return dataset, class_names, file_paths, labels

def create_data_generators():
    """
    Create training and validation datasets
    
    Returns:
        tuple: (train_ds, val_ds, class_names)
    """
    print("Creating training dataset...")
    train_ds, class_names, _, _ = load_dataset_from_directory(
        config.TRAIN_DIR, 
        batch_size=config.BATCH_SIZE,
        shuffle=True
    )
    
    print("Creating validation dataset...")
    val_ds, val_class_names, _, _ = load_dataset_from_directory(
        config.VAL_DIR, 
        batch_size=config.BATCH_SIZE,
        shuffle=False
    )
    
    # Verify classes match
    if class_names != val_class_names:
        print("Warning: Training and validation classes do not match exactly!")
        print(f"Train: {class_names}")
        print(f"Val: {val_class_names}")
    
    return train_ds, val_ds, class_names


def get_class_weights(train_ds):
    """
    Calculate class weights for imbalanced datasets
    
    Args:
        train_ds: Training dataset
        
    Returns:
        dict: Class weights
    """
    from sklearn.utils.class_weight import compute_class_weight
    
    # Let's use a helper to get labels from directory again
    labels = []
    classes_set = set()
    
    # Scan directory to find classes
    for pet_type in os.listdir(config.TRAIN_DIR):
        pet_type_dir = os.path.join(config.TRAIN_DIR, pet_type)
        if os.path.isdir(pet_type_dir):
            for breed in os.listdir(pet_type_dir):
                breed_dir = os.path.join(pet_type_dir, breed)
                if os.path.isdir(breed_dir):
                    class_path = f"{pet_type}/{breed}"
                    classes_set.add(class_path)
    
    class_names = sorted(list(classes_set))
    class_to_index = {cls: i for i, cls in enumerate(class_names)}
    
    # Collect labels
    for pet_type in os.listdir(config.TRAIN_DIR):
        pet_type_dir = os.path.join(config.TRAIN_DIR, pet_type)
        if os.path.isdir(pet_type_dir):
            for breed in os.listdir(pet_type_dir):
                breed_dir = os.path.join(pet_type_dir, breed)
                if os.path.isdir(breed_dir):
                    class_path = f"{pet_type}/{breed}"
                    if class_path in class_to_index:
                        cls_idx = class_to_index[class_path]
                        # Count files
                        count = len([f for f in os.listdir(breed_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                        labels.extend([cls_idx] * count)

    if not labels:
        return {}

    # Compute class weights
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    
    # Convert to dictionary
    class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
    
    print(f"Class weights: {class_weight_dict}")
    
    return class_weight_dict


def preprocess_image(image_path, img_size=config.IMG_SIZE):
    """
    Preprocess a single image for prediction
    
    Args:
        image_path: Path to image file
        img_size: Target image size
        
    Returns:
        numpy array: Preprocessed image
    """
    img = tf.keras.preprocessing.image.load_img(
        image_path,
        target_size=(img_size, img_size)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    # EfficientNet expects [0, 255]
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    
    return img_array


def preprocess_image_from_bytes(image_bytes, img_size=config.IMG_SIZE):
    """
    Preprocess image from bytes (for FastAPI integration)
    
    Args:
        image_bytes: Raw image bytes
        img_size: Target image size
        
    Returns:
        numpy array: Preprocessed image
    """
    from PIL import Image
    import io
    
    # Open image from bytes
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize
    img = img.resize((img_size, img_size))
    
    # Convert to array
    img_array = np.array(img)
    # EfficientNet expects [0, 255]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    return img_array
