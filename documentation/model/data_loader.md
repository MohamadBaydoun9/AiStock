# Data Loader Documentation (`data_loader.py`)

**Role:** Data Pipeline & Preprocessing.

This module handles loading images from the disk, applying preprocessing, and creating optimized TensorFlow Datasets.

## Key Functions

### 1. `load_dataset_from_directory`
- **Scans Directory**: Recursively finds images in `ml/data/train` or `ml/data/val`.
- **Supports Hierarchy**: Handles both flat (`Class/img.jpg`) and nested (`Type/Breed/img.jpg`) directory structures.
- **Labeling**: Automatically assigns integer labels to classes and converts them to One-Hot Encoding.
- **Performance**: Uses `tf.data.Dataset` API with `prefetch` and `AUTOTUNE` for high-performance parallel loading.

### 2. `process_path`
- **Image Loading**: Reads raw bytes and decodes JPEGs/PNGs.
- **Resizing**: Resizes images to `(224, 224)`.
- **Note**: EfficientNet expects `[0, 255]` pixel values, so no division by 255 is performed here (unlike some other models).

### 3. `get_class_weights`
- **Purpose**: Handles class imbalance.
- **Logic**: Calculates weights such that rare breeds have a higher impact on the loss function than common breeds. This prevents the model from being biased towards the majority class.

### 4. `preprocess_image_from_bytes`
- **Usage**: Used by the FastAPI backend (`predict.py`) to process images uploaded by users directly from memory, without saving them to disk first.
