# Dataset Generation Documentation (`generate_price_dataset.py`)

**Role:** Synthetic Data Generator.

Since real-world pet pricing data is scarce and unstructured, this script generates a realistic synthetic dataset to train the price prediction model.

## Logic

1.  **Scanning**: Scans the `ml/data/train` and `ml/data/val` directories to identify all available breeds in the system.
2.  **Rules Engine**:
    - Uses a dictionary `BREED_CHARACTERISTICS` to define base price, average weight, and price variance for each breed.
    - Uses `BREED_COUNTRY_MAP` to assign plausible countries of origin.
    - Uses `COUNTRY_MULTIPLIERS` to adjust price based on origin (e.g., "Imported from Japan" > "Local").
3.  **Randomization**:
    - Generates random but realistic ages (skewed towards younger pets).
    - Varies weight around the breed average.
    - Randomly assigns health and vaccination status.
4.  **Price Calculation**:
    - Applies multipliers for Age (younger = expensive), Health, Vaccination, and Country.
    - Adds random noise to simulate market fluctuations.
5.  **Output**: Saves the generated dataset to `ml/data/price_training_data.csv`.

## Usage
Run this script whenever you add new breeds to the image dataset to include them in the price model.
```bash
python ml/generate_price_dataset.py
```
