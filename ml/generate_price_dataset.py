"""
Generate synthetic price training dataset from existing image data
"""
import os
import random
import pandas as pd
import config

# Breed-specific characteristics for realistic data generation (2024/2025 Market Prices)
BREED_CHARACTERISTICS = {
    # --------------------
    # DOGS
    # --------------------
    'Afghan': {
        'avg_weight': 25,     # kg
        'base_price': 2200,   # USD
        'price_range': 600
    },
    'African Wild Dog': {
        'avg_weight': 23,
        'base_price': 5000,   # very exotic / not typical pet
        'price_range': 1500
    },
    'Akita Inu': {
        'avg_weight': 32,
        'base_price': 2600,
        'price_range': 700
    },
    'Bermaise': {  # Bernese Mountain Dog (folder spelling)
        'avg_weight': 40,
        'base_price': 2500,
        'price_range': 700
    },
    'Boston Terrier': {
        'avg_weight': 9,
        'base_price': 1500,
        'price_range': 400
    },
    'bulldog': {  # folder name is lowercase
        'avg_weight': 22,
        'base_price': 3000,
        'price_range': 800
    },
    'Chow': {  # Chow Chow
        'avg_weight': 25,
        'base_price': 2300,
        'price_range': 600
    },
    'Elk Hound': {  # Norwegian Elkhound type
        'avg_weight': 23,
        'base_price': 1800,
        'price_range': 500
    },
    'German Sheperd': {  # keep folder spelling
        'avg_weight': 35,
        'base_price': 2000,
        'price_range': 500
    },
    'japanese': {  # generic Japanese small dog (folder name)
        'avg_weight': 8,
        'base_price': 1700,
        'price_range': 400
    },
    'Maltese': {
        'avg_weight': 4,
        'base_price': 1600,
        'price_range': 400
    },
    'Pekinese': {  # Pekingese
        'avg_weight': 5,
        'base_price': 1400,
        'price_range': 400
    },
    'Shiba Inu': {
        'avg_weight': 10,
        'base_price': 2400,
        'price_range': 600
    },
    'Shih-Tzu': {
        'avg_weight': 6,
        'base_price': 1500,
        'price_range': 400
    },

    # --------------------
    # CATS
    # --------------------
    'Abyssinian': {
        'avg_weight': 4.5,
        'base_price': 1600,
        'price_range': 400
    },
    'American Bobtail': {
        'avg_weight': 5.5,
        'base_price': 1300,
        'price_range': 300
    },
    'American Curl': {
        'avg_weight': 4.5,
        'base_price': 1400,
        'price_range': 350
    },
    'Burmese': {
        'avg_weight': 4.5,
        'base_price': 1200,
        'price_range': 300
    },
    'Domestic Short Hair': {
        'avg_weight': 4.5,
        'base_price': 300,    # common / shelter cat
        'price_range': 150
    },
    'Exotic Shorthair': {
        'avg_weight': 5,
        'base_price': 1800,
        'price_range': 500
    },
    'Maine Coon': {
        'avg_weight': 7,
        'base_price': 1600,   # typical 1000–2000 range
        'price_range': 500
    },
    'Oriental Long Hair': {
        'avg_weight': 4.5,
        'base_price': 1500,
        'price_range': 400
    },
    'Scottish Fold': {
        'avg_weight': 4.5,
        'base_price': 1700,
        'price_range': 450
    },
    'Siberian': {
        'avg_weight': 6,
        'base_price': 1700,
        'price_range': 450
    },
    'Tortoiseshell': {
        'avg_weight': 4.5,
        'base_price': 350,    # color pattern, often mixed-breed
        'price_range': 150
    },

    # --------------------
    # BIRDS
    # --------------------
    'AMERICAN GOLDFINCH': {
        'avg_weight': 0.02,
        'base_price': 80,
        'price_range': 40
    },
    'BARN OWL': {
        'avg_weight': 0.5,
        'base_price': 1800,
        'price_range': 600
    },
    'CARMINE BEE-EATER': {
        'avg_weight': 0.05,
        'base_price': 900,
        'price_range': 300
    },
    'DOWNY WOODPECKER': {
        'avg_weight': 0.03,
        'base_price': 200,
        'price_range': 100
    },

    # --------------------
    # MONKEYS
    # --------------------
    'Bald Uakari': {
        'avg_weight': 3.0,
        'base_price': 9000,   # very rare / exotic
        'price_range': 2500
    },
    'Emperor Tamarin': {
        'avg_weight': 0.5,
        'base_price': 2200,   # similar to tamarin ranges
        'price_range': 600
    },
    'Golden Monkey': {
        'avg_weight': 6.0,
        'base_price': 10000,
        'price_range': 3000
    },
    'Hamadryas Baboon': {
        'avg_weight': 20.0,
        'base_price': 5000,
        'price_range': 1500
    },
    'Mandril': {
        'avg_weight': 25.0,
        'base_price': 12000,
        'price_range': 3500
    },
    'Proboscis Monkey': {
        'avg_weight': 18.0,
        'base_price': 11000,
        'price_range': 3000
    },
    'Red Howler': {
        'avg_weight': 7.0,
        'base_price': 8000,
        'price_range': 2500
    },
    'White Faced Saki': {
        'avg_weight': 2.0,
        'base_price': 8500,
        'price_range': 2500
    },

    # --------------------
    # FISH
    # --------------------
    'Anthias anthias': {
        'avg_weight': 0.2,
        'base_price': 25,
        'price_range': 15
    },
    'Coris julis': {
        'avg_weight': 0.15,
        'base_price': 15,
        'price_range': 10
    },
    'Dasyatis centroura': {  # stingray
        'avg_weight': 10.0,
        'base_price': 200,
        'price_range': 100
    },
    'Gobius niger': {
        'avg_weight': 0.1,
        'base_price': 10,
        'price_range': 5
    },
    'Gold Fish': {
        'avg_weight': 0.2,
        'base_price': 20,
        'price_range': 10
    },
    'Polyprion americanus': {  # wreckfish
        'avg_weight': 5.0,
        'base_price': 50,
        'price_range': 25
    },
    'Rhinobatos cemiculus': {  # guitarfish
        'avg_weight': 8.0,
        'base_price': 80,
        'price_range': 40
    },
    'Solea solea': {
        'avg_weight': 0.5,
        'base_price': 30,
        'price_range': 15
    },
    'Tetrapturus belone': {  # Mediterranean spearfish
        'avg_weight': 20.0,
        'base_price': 150,
        'price_range': 100
    },
    'Trigloporus lastoviza': {  # gurnard
        'avg_weight': 0.5,
        'base_price': 20,
        'price_range': 10
    },
}

BREED_COUNTRY_MAP = {
    # --------------------
    # DOGS
    # --------------------
    'Afghan': ['Afghanistan', 'USA', 'England'],
    'African Wild Dog': ['Africa', 'USA'],
    'Akita Inu': ['Japan', 'USA'],
    'Bermaise': ['Switzerland', 'USA'],       # Bernese origin, but country not in multipliers (falls back to 1.0)
    'Boston Terrier': ['USA', 'Canada'],
    'bulldog': ['England', 'USA', 'France'],
    'Chow': ['China', 'USA'],
    'Elk Hound': ['Norway', 'USA'],
    'German Sheperd': ['Germany', 'USA', 'England'],
    'japanese': ['Japan', 'USA'],
    'Maltese': ['Malta', 'England', 'USA'],
    'Pekinese': ['China', 'USA'],
    'Shiba Inu': ['Japan', 'USA'],
    'Shih-Tzu': ['China', 'USA', 'England'],

    # --------------------
    # CATS
    # --------------------
    'Abyssinian': ['Ethiopia', 'England', 'USA'],
    'American Bobtail': ['USA', 'Canada'],
    'American Curl': ['USA', 'Canada'],
    'Burmese': ['Myanmar', 'England', 'USA'],
    'Domestic Short Hair': ['USA', 'England'],
    'Exotic Shorthair': ['USA', 'England'],
    'Maine Coon': ['USA', 'Canada', 'England'],
    'Oriental Long Hair': ['England', 'USA'],
    'Scottish Fold': ['Scotland', 'England', 'USA'],
    'Siberian': ['Russia', 'USA'],
    'Tortoiseshell': ['USA', 'England'],

    # --------------------
    # BIRDS
    # --------------------
    'AMERICAN GOLDFINCH': ['USA', 'Canada'],
    'BARN OWL': ['England', 'USA'],
    'CARMINE BEE-EATER': ['Africa', 'South Africa'],
    'DOWNY WOODPECKER': ['USA', 'Canada'],

    # --------------------
    # MONKEYS
    # --------------------
    'Bald Uakari': ['Brazil', 'Colombia'],
    'Emperor Tamarin': ['Brazil', 'Peru'],
    'Golden Monkey': ['China'],
    'Hamadryas Baboon': ['Ethiopia', 'Yemen'],
    'Mandril': ['Gabon', 'Cameroon'],
    'Proboscis Monkey': ['Indonesia'],
    'Red Howler': ['Brazil', 'Peru'],
    'White Faced Saki': ['Brazil', 'Guyana'],

    # --------------------
    # FISH
    # --------------------
    'Anthias anthias': ['Italy', 'Greece'],
    'Coris julis': ['Spain', 'Portugal', 'Italy'],
    'Dasyatis centroura': ['USA', 'Brazil'],
    'Gobius niger': ['Italy', 'Greece'],
    'Gold Fish': ['China', 'Japan', 'USA'],
    'Polyprion americanus': ['Portugal', 'USA', 'Brazil'],
    'Rhinobatos cemiculus': ['Spain', 'Morocco'],
    'Solea solea': ['Spain', 'Italy', 'France'],
    'Tetrapturus belone': ['Italy', 'Greece'],
    'Trigloporus lastoviza': ['Italy', 'Greece', 'Turkey'],
}

# Country price multipliers (rarity/prestige factor)
COUNTRY_MULTIPLIERS = {
    'Afghanistan': 1.15,  # Exotic/rare
    'Africa': 1.20,       # Very exotic
    'Scotland': 1.05,     # Prestige
    'Canada': 1.02,       # Standard
    'Germany': 1.08,      # Quality reputation
    'England': 1.10,      # Prestige
    'France': 1.07,       # Prestige
    'Russia': 1.12,       # Exotic
    'Wales': 1.06,        # Prestige
    'Ethiopia': 1.15,     # Exotic
    'USA': 1.00,          # Base/standard
    'Iran': 1.18,         # Exotic/prestigious (Persian cats)
    'Thailand': 1.12,     # Exotic
    'China': 1.05,
    'Japan': 1.10,
    'Australia': 1.15,
    'Brazil': 1.12,
    'Indonesia': 1.08,
    'Spain': 1.05,
    # Any countries not listed here default to multiplier 1.0 in generate_metadata
}

# Helper to normalize names for matching (e.g. "Gold Fish" -> "goldfish")
def normalize_name(name):
    return name.lower().replace(" ", "").replace("_", "")

# Create normalized lookup tables
NORMALIZED_BREED_CHARS = {normalize_name(k): v for k, v in BREED_CHARACTERISTICS.items()}
NORMALIZED_COUNTRY_MAP = {normalize_name(k): v for k, v in BREED_COUNTRY_MAP.items()}

def generate_metadata(pet_type, breed):
    """
    Generate realistic metadata for a pet

    Args:
        pet_type: Dog / Cat / Bird / Fish / Monkey
        breed: Breed name (folder name)

    Returns:
        dict: Metadata including age, weight, health, vaccination, country, price
    """
    # Get breed characteristics or use defaults
    default_weight = 20
    if pet_type == 'Cat':
        default_weight = 5
    elif pet_type == 'Fish':
        default_weight = 0.1
    elif pet_type == 'Bird':
        default_weight = 0.2
    elif pet_type == 'Monkey':
        default_weight = 5

    # Try to find breed using normalized name
    normalized_breed = normalize_name(breed)
    breed_info = NORMALIZED_BREED_CHARS.get(normalized_breed)

    # If not found, use defaults
    if not breed_info:
        breed_info = {
            'avg_weight': default_weight,
            'base_price': 1000,
            'price_range': 300
        }

    # Get country of origin (randomly select from possible countries)
    possible_countries = NORMALIZED_COUNTRY_MAP.get(normalized_breed, ['USA'])  # Default to USA
    country = random.choice(possible_countries)
    country_multiplier = COUNTRY_MULTIPLIERS.get(country, 1.0)

    # Generate age (2-60 months, with bias towards younger)
    age_months = random.choices(
        range(2, 61),
        weights=[3 if i < 12 else 2 if i < 24 else 1 for i in range(2, 61)]
    )[0]

    # Generate weight with some variation around breed average
    weight = max(0.1, breed_info['avg_weight'] + random.uniform(-0.2, 0.2) * breed_info['avg_weight'])
    weight = round(weight, 2)

    # Health status (0=normal, 1=good, 2=excellent)
    health_status = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]

    # Vaccination status
    vaccinated = random.choices([0, 1], weights=[0.15, 0.85])[0]

    # Calculate price based on factors
    base_price = breed_info['base_price']
    price_range = breed_info['price_range']

    # Price factors:
    age_factor = 1.3 if age_months < 6 else 1.1 if age_months < 12 else 1.0 if age_months < 24 else 0.85
    health_bonus = health_status * 100
    vaccination_bonus = 150 if vaccinated else 0
    country_bonus = (base_price * (country_multiplier - 1.0))

    # Final price with some randomness
    price = base_price * age_factor + health_bonus + vaccination_bonus + country_bonus
    price += random.uniform(-price_range / 2, price_range / 2)
    price = max(100, round(price, 2))  # Minimum $100

    return {
        'age_months': age_months,
        'weight': weight,
        'health_status': health_status,
        'vaccinated': vaccinated,
        'country': country,
        'price': price
    }

def scan_directory_and_generate_dataset(base_dir, dataset_name):
    """
    Scan directory and generate dataset rows

    Args:
        base_dir: Directory to scan (train or val)
        dataset_name: Name for logging (train/val)

    Returns:
        list: List of data rows
    """
    data_rows = []

    if not os.path.exists(base_dir):
        print(f"Warning: {base_dir} does not exist")
        return data_rows

    # Scan Type/Breed/image.jpg structure
    for pet_type in os.listdir(base_dir):
        pet_type_dir = os.path.join(base_dir, pet_type)

        if not os.path.isdir(pet_type_dir):
            continue

        for breed in os.listdir(pet_type_dir):
            breed_dir = os.path.join(pet_type_dir, breed)

            if not os.path.isdir(breed_dir):
                continue

            # Process all images in breed directory
            for image_file in os.listdir(breed_dir):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Generate metadata
                    metadata = generate_metadata(pet_type, breed)

                    # Create row (NO image_path)
                    row = {
                        'type': pet_type,
                        'breed': breed,
                        **metadata
                    }

                    data_rows.append(row)

    print(f"Generated {len(data_rows)} samples from {dataset_name}")
    return data_rows

def main():
    """Generate synthetic price dataset"""
    print("=" * 60)
    print("Generating Synthetic Price Dataset (Metadata Only)")
    print("=" * 60)

    # Collect data from train and val directories
    all_data = []

    print("\n📁 Scanning training data...")
    train_data = scan_directory_and_generate_dataset(config.TRAIN_DIR, 'train')
    all_data.extend(train_data)

    print("\n📁 Scanning validation data...")
    val_data = scan_directory_and_generate_dataset(config.VAL_DIR, 'val')
    all_data.extend(val_data)

    if not all_data:
        print("\n❌ No images found! Please ensure ml/data/train and ml/data/val contain images.")
        return

    # Create DataFrame
    df = pd.DataFrame(all_data)

    # Show statistics
    print("\n" + "=" * 60)
    print("Dataset Statistics")
    print("=" * 60)
    print(f"Total samples: {len(df)}")
    print(f"\nBreed distribution:")
    print(df['breed'].value_counts())
    print(f"\nCountry distribution:")
    print(df['country'].value_counts())
    print(f"\nPrice statistics:")
    print(df['price'].describe())
    print(f"\nHealth status distribution:")
    print(df['health_status'].value_counts())
    print(f"\nVaccination rate: {df['vaccinated'].mean() * 100:.1f}%")

    # Save to CSV
    output_path = os.path.join(config.DATA_DIR, 'price_training_data.csv')
    df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset saved to: {output_path}")
    print(f"   Columns: {list(df.columns)}")
    print("\nYou can now train the price prediction model with:")
    print("   python ml/train_price_model.py")

if __name__ == '__main__':
    main()
