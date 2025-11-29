"""
Generate synthetic price training dataset from existing image data
"""
import os
import random
import pandas as pd
import config

# Breed-specific characteristics for realistic data generation
BREED_CHARACTERISTICS = {
    # Dogs
    'Afghan': {'avg_weight': 25, 'base_price': 1800, 'price_range': 400},
    'African Wild Dog': {'avg_weight': 23, 'base_price': 2500, 'price_range': 500},
    'Golden Retriever': {'avg_weight': 30, 'base_price': 1500, 'price_range': 300},
    'Labrador': {'avg_weight': 32, 'base_price': 1200, 'price_range': 300},
    'German Shepherd': {'avg_weight': 35, 'base_price': 1800, 'price_range': 400},
    'Bulldog': {'avg_weight': 22, 'base_price': 2000, 'price_range': 500},
    'Poodle': {'avg_weight': 25, 'base_price': 1600, 'price_range': 400},
    'Beagle': {'avg_weight': 12, 'base_price': 1000, 'price_range': 200},
    'Husky': {'avg_weight': 23, 'base_price': 1700, 'price_range': 400},
    'Corgi': {'avg_weight': 13, 'base_price': 1400, 'price_range': 300},
    
    # Cats
    'Abyssinian': {'avg_weight': 4.5, 'base_price': 900, 'price_range': 200},
    'American Bobtail': {'avg_weight': 5.5, 'base_price': 800, 'price_range': 200},
    'Persian': {'avg_weight': 5, 'base_price': 1200, 'price_range': 300},
    'Siamese': {'avg_weight': 4, 'base_price': 900, 'price_range': 200},
    'Maine Coon': {'avg_weight': 7, 'base_price': 900, 'price_range': 250},
    'Bengal': {'avg_weight': 5.5, 'base_price': 1200, 'price_range': 300},
    'Ragdoll': {'avg_weight': 6.5, 'base_price': 850, 'price_range': 200},
    'British Shorthair': {'avg_weight': 5.5, 'base_price': 700, 'price_range': 150},
    'Sphynx': {'avg_weight': 4, 'base_price': 1500, 'price_range': 400},
    'Scottish Fold': {'avg_weight': 4.5, 'base_price': 1000, 'price_range': 250},

    # Fish
    'Goldfish': {'avg_weight': 0.2, 'base_price': 20, 'price_range': 15},
    'Betta': {'avg_weight': 0.05, 'base_price': 15, 'price_range': 10},
    'Clownfish': {'avg_weight': 0.1, 'base_price': 30, 'price_range': 10},
    'Guppy': {'avg_weight': 0.02, 'base_price': 5, 'price_range': 3},
    'Angelfish': {'avg_weight': 0.15, 'base_price': 25, 'price_range': 10},

    # Birds
    'Parrot': {'avg_weight': 0.5, 'base_price': 500, 'price_range': 200},
    'Canary': {'avg_weight': 0.02, 'base_price': 80, 'price_range': 30},
    'Cockatiel': {'avg_weight': 0.1, 'base_price': 150, 'price_range': 50},
    'Parakeet': {'avg_weight': 0.04, 'base_price': 40, 'price_range': 20},
    'Finch': {'avg_weight': 0.02, 'base_price': 30, 'price_range': 15},

    # Monkeys
    'Capuchin': {'avg_weight': 3.5, 'base_price': 6000, 'price_range': 1000},
    'Macaque': {'avg_weight': 6.0, 'base_price': 5000, 'price_range': 800},
    'Marmoset': {'avg_weight': 0.4, 'base_price': 4000, 'price_range': 600},
    'Spider Monkey': {'avg_weight': 7.0, 'base_price': 7000, 'price_range': 1200},
    'Tamarin': {'avg_weight': 0.5, 'base_price': 4500, 'price_range': 700},
}

# Breed-to-country mapping (possible countries of origin/breeding)
# Each breed can come from 2-5 countries
BREED_COUNTRY_MAP = {
    # Dogs
    'Afghan': ['Afghanistan', 'USA', 'England'],
    'African Wild Dog': ['Africa', 'USA'],
    'Golden Retriever': ['Scotland', 'USA', 'Canada', 'England'],
    'Labrador': ['Canada', 'USA', 'England'],
    'German Shepherd': ['Germany', 'USA', 'England'],
    'Bulldog': ['England', 'USA', 'France'],
    'Poodle': ['France', 'USA', 'England', 'Germany'],
    'Beagle': ['England', 'USA', 'Canada'],
    'Husky': ['Russia', 'USA', 'Canada'],
    'Corgi': ['Wales', 'England', 'USA'],
    
    # Cats
    'Abyssinian': ['Ethiopia', 'England', 'USA'],
    'American Bobtail': ['USA', 'Canada'],
    'Persian': ['Iran', 'USA', 'England', 'France'],
    'Siamese': ['Thailand', 'USA', 'England'],
    'Maine Coon': ['USA', 'Canada', 'England'],
    'Bengal': ['USA', 'England', 'Canada'],
    'Ragdoll': ['USA', 'England', 'Canada'],
    'British Shorthair': ['England', 'USA', 'France'],
    'Sphynx': ['Canada', 'USA', 'England'],
    'Scottish Fold': ['Scotland', 'England', 'USA'],

    # Fish
    'Goldfish': ['China', 'Japan', 'USA'],
    'Betta': ['Thailand', 'Vietnam', 'USA'],
    'Clownfish': ['Australia', 'Indonesia', 'USA'],
    'Guppy': ['Brazil', 'Venezuela', 'USA'],
    'Angelfish': ['Brazil', 'Peru', 'USA'],

    # Birds
    'Parrot': ['Brazil', 'Australia', 'USA'],
    'Canary': ['Spain', 'Germany', 'USA'],
    'Cockatiel': ['Australia', 'USA'],
    'Parakeet': ['Australia', 'USA'],
    'Finch': ['Australia', 'USA'],

    # Monkeys
    'Capuchin': ['Brazil', 'Colombia', 'USA'],
    'Macaque': ['China', 'Japan', 'USA'],
    'Marmoset': ['Brazil', 'USA'],
    'Spider Monkey': ['Brazil', 'Mexico', 'USA'],
    'Tamarin': ['Brazil', 'Colombia', 'USA'],
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
    'Thailand': 1.12,     # Exotic (Siamese/Betta)
    'China': 1.05,        # Goldfish origin
    'Japan': 1.10,        # Koi/Goldfish quality
    'Australia': 1.15,    # Exotic birds/fish
    'Brazil': 1.12,       # Amazonian exotics
    'Indonesia': 1.08,    # Tropical fish
    'Spain': 1.05,        # Canaries
}

def generate_metadata(pet_type, breed):
    """
    Generate realistic metadata for a pet
    
    Args:
        pet_type: Dog or Cat
        breed: Breed name
        
    Returns:
        dict: Metadata including age, weight, health, vaccination, country, price
    """
    # Get breed characteristics or use defaults
    default_weight = 20
    if pet_type == 'Cat': default_weight = 5
    elif pet_type == 'Fish': default_weight = 0.1
    elif pet_type == 'Bird': default_weight = 0.2
    elif pet_type == 'Monkey': default_weight = 5
    
    breed_info = BREED_CHARACTERISTICS.get(breed, {
        'avg_weight': default_weight,
        'base_price': 1000,
        'price_range': 300
    })
    
    # Get country of origin (randomly select from possible countries)
    possible_countries = BREED_COUNTRY_MAP.get(breed, ['USA'])  # Default to USA
    country = random.choice(possible_countries)
    country_multiplier = COUNTRY_MULTIPLIERS.get(country, 1.0)
    
    # Generate age (2-60 months, with bias towards younger)
    # Younger pets are typically more expensive
    age_months = random.choices(
        range(2, 61),
        weights=[3 if i < 12 else 2 if i < 24 else 1 for i in range(2, 61)]
    )[0]
    
    # Generate weight with some variation around breed average
    weight = max(1, breed_info['avg_weight'] + random.uniform(-0.2, 0.2) * breed_info['avg_weight'])
    weight = round(weight, 2)
    
    # Health status (0=normal, 1=good, 2=excellent)
    health_status = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
    
    # Vaccination status
    vaccinated = random.choices([0, 1], weights=[0.15, 0.85])[0]
    
    # Calculate price based on factors
    base_price = breed_info['base_price']
    price_range = breed_info['price_range']
    
    # Price factors:
    # - Younger pets are more valuable (puppies/kittens)
    age_factor = 1.3 if age_months < 6 else 1.1 if age_months < 12 else 1.0 if age_months < 24 else 0.85
    
    # - Excellent health adds value
    health_bonus = health_status * 100
    
    # - Vaccination adds value
    vaccination_bonus = 150 if vaccinated else 0
    
    # - Country premium (exotic/prestigious origins cost more)
    country_bonus = (base_price * (country_multiplier - 1.0))
    
    # Calculate final price with some randomness
    price = base_price * age_factor + health_bonus + vaccination_bonus + country_bonus
    price += random.uniform(-price_range/2, price_range/2)
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
                    # Get relative path from project root
                    image_path = os.path.join(breed_dir, image_file)
                    
                    # Generate metadata
                    metadata = generate_metadata(pet_type, breed)
                    
                    # Create row
                    row = {
                        'image_path': image_path,
                        'type': pet_type,
                        'breed': breed,
                        **metadata
                    }
                    
                    data_rows.append(row)
    
    print(f"Found {len(data_rows)} images in {dataset_name}")
    return data_rows

def main():
    """Generate synthetic price dataset"""
    print("=" * 60)
    print("Generating Synthetic Price Dataset with Country")
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
    print(f"\nVaccination rate: {df['vaccinated'].mean()*100:.1f}%")
    
    # Save to CSV
    output_path = os.path.join(config.DATA_DIR, 'price_training_data.csv')
    df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset saved to: {output_path}")
    print(f"   Columns: {list(df.columns)}")
    print("\nYou can now train the price prediction model with:")
    print("   python ml/train_price_model.py")

if __name__ == '__main__':
    main()
