"""
Data Splitter Script
Extracts test and validation images from training data for a given pet type

Usage:
    python datasplitter.py Fish
    python datasplitter.py Bird
    python datasplitter.py Monkey
"""
import os
import sys
import shutil
import random
from pathlib import Path

def split_data(type_folder_name, test_images_per_breed=5, val_ratio=0.2):
    """
    Split training data into train/val/test sets
    
    Args:
        type_folder_name: Name of the pet type folder (e.g., 'Fish', 'Bird', 'Monkey')
        test_images_per_breed: Number of images to extract for test set (default: 5)
        val_ratio: Ratio of remaining images to use for validation (default: 0.2 = 20%)
    """
    # Get ml directory
    ml_dir = Path(__file__).parent
    data_dir = ml_dir / 'data'
    train_dir = data_dir / 'train' / type_folder_name
    
    # Check if training folder exists
    if not train_dir.exists():
        print(f"❌ Error: Training folder not found: {train_dir}")
        print(f"   Please ensure {type_folder_name} folder exists in ml/data/train/")
        return False
    
    # Create extracted folders
    extracted_base = data_dir / 'train' / 'extracted' / type_folder_name
    test_dir = extracted_base / 'test'
    val_dir = extracted_base / 'val'
    
    # Create directories
    test_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print(f"Data Splitter - {type_folder_name}")
    print("=" * 70)
    print(f"\nSource: {train_dir}")
    print(f"Test output: {test_dir}")
    print(f"Val output: {val_dir}")
    print(f"\nConfiguration:")
    print(f"  - Test images per breed: {test_images_per_breed}")
    print(f"  - Validation ratio: {val_ratio * 100}%")
    print(f"  - Training ratio: {(1 - val_ratio) * 100}%")
    print()
    
    # Process each breed subfolder
    breed_folders = [f for f in train_dir.iterdir() if f.is_dir()]
    
    if not breed_folders:
        print(f"❌ Error: No breed subfolders found in {train_dir}")
        return False
    
    print(f"Found {len(breed_folders)} breed folders\n")
    
    total_test = 0
    total_val = 0
    total_train = 0
    
    for breed_folder in sorted(breed_folders):
        breed_name = breed_folder.name
        print(f"📁 Processing: {breed_name}")
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
        all_images = [
            f for f in breed_folder.iterdir() 
            if f.is_file() and f.suffix in image_extensions
        ]
        
        if len(all_images) < test_images_per_breed + 1:
            print(f"   ⚠️  Warning: Only {len(all_images)} images found. Skipping (need at least {test_images_per_breed + 1})")
            continue
        
        # Shuffle images randomly
        random.shuffle(all_images)
        
        # Extract test images (first N images)
        test_images = all_images[:test_images_per_breed]
        remaining_images = all_images[test_images_per_breed:]
        
        # Calculate validation count from remaining images
        val_count = max(1, int(len(remaining_images) * val_ratio))
        val_images = remaining_images[:val_count]
        train_images = remaining_images[val_count:]
        
        # Create breed folders in test and val
        breed_test_dir = test_dir / breed_name
        breed_val_dir = val_dir / breed_name
        breed_test_dir.mkdir(exist_ok=True)
        breed_val_dir.mkdir(exist_ok=True)
        
        # Copy test images
        for img in test_images:
            shutil.copy2(img, breed_test_dir / img.name)
        
        # Copy validation images
        for img in val_images:
            shutil.copy2(img, breed_val_dir / img.name)
        
        # Update counters
        total_test += len(test_images)
        total_val += len(val_images)
        total_train += len(train_images)
        
        print(f"   ✓ Total: {len(all_images)} images")
        print(f"   ├─ Test: {len(test_images)} images → {breed_test_dir}")
        print(f"   ├─ Val: {len(val_images)} images → {breed_val_dir}")
        print(f"   └─ Train: {len(train_images)} images (remaining in original folder)")
        print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total images extracted:")
    print(f"  ✓ Test: {total_test} images")
    print(f"  ✓ Validation: {total_val} images")
    print(f"  ✓ Training: {total_train} images (kept in original folders)")
    print(f"\nTotal: {total_test + total_val + total_train} images")
    print(f"\n✅ Extraction complete!")
    print(f"\nExtracted files location:")
    print(f"  📂 {extracted_base}")
    print(f"\n💡 Next steps:")
    print(f"  1. Move test images: mv {test_dir} {data_dir / 'test' / type_folder_name}")
    print(f"  2. Move val images: mv {val_dir} {data_dir / 'val' / type_folder_name}")
    print(f"  3. Or keep them in extracted folder for review first")
    
    return True

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python datasplitter.py <type_folder_name>")
        print("\nExamples:")
        print("  python datasplitter.py Fish")
        print("  python datasplitter.py Bird")
        print("  python datasplitter.py Monkey")
        print("\nOptional arguments:")
        print("  python datasplitter.py Fish 10      # Extract 10 test images per breed")
        print("  python datasplitter.py Fish 5 0.25  # 5 test images, 25% validation")
        sys.exit(1)
    
    type_folder_name = sys.argv[1]
    
    # Optional arguments
    test_images_per_breed = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    val_ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Run splitter
    success = split_data(type_folder_name, test_images_per_breed, val_ratio)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
