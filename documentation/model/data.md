# Data Directory Documentation

The `ml/data` directory is the central storage for all datasets used to train and validate the machine learning models.

## Directory Structure

```
ml/data/
├── train/                  # Training Dataset (80%)
│   ├── Dog/                # Product Type Category
│   │   ├── Golden Retriever/
│   │   │   ├── img1.jpg
│   │   │   └── ...
│   │   └── ...
│   └── Cat/
│       ├── Persian/
│       └── ...
├── val/                    # Validation Dataset (20%)
│   ├── Dog/
│   │   └── ...
│   └── Cat/
│       └── ...
└── price_training_data.csv # Synthetic Metadata Dataset
```

## 1. Image Data (`train/` & `val/`)
**Purpose:** Used to train the **Pet Breed Classification Model** (`EfficientNetB0`).

**Structure:**
- **Hierarchical Organization**: Images are organized first by **Product Type** (e.g., "Dog", "Cat") and then by **Breed** (e.g., "Golden Retriever", "Siamese").
- **Format**: Supports `.jpg`, `.jpeg`, `.png`.
- **Preprocessing**: Images are resized to `224x224` pixels and normalized to `[0, 255]` range (as expected by EfficientNet) during loading.

**Data Split:**
- **Train**: Used to update model weights.
- **Val**: Used to evaluate model performance during training and trigger early stopping if overfitting occurs.

## 2. Metadata (`price_training_data.csv`)
**Purpose:** Used to train the **Price Prediction Model**.

**Generation:**
- Created by `ml/generate_price_dataset.py`.
- It scans the image directories to determine available breeds.
- It generates synthetic but realistic market data (price, age, weight, health status) based on predefined rules in the script.

**Columns:**
- `type`: Pet type (Dog, Cat).
- `breed`: Specific breed name.
- `age_months`: Age of the pet.
- `weight`: Weight in kg.
- `health_status`: 0 (Normal), 1 (Good), 2 (Excellent).
- `vaccinated`: 0 (No), 1 (Yes).
- `country`: Country of origin.
- `price`: Target variable (Market price in USD).
