"""
Find and Remove Corrupted Images from Dataset
"""
import os
from PIL import Image
from pathlib import Path
import shutil

def check_image(image_path):
    """
    Check if an image file is valid and readable
    
    Args:
        image_path: Path to image file
        
    Returns:
        bool: True if valid, False if corrupted
    """
    try:
        img = Image.open(image_path)
        img.verify()  # Verify it's a valid image
        
        # Try to load and resize (catches more issues)
        img = Image.open(image_path)
        img.resize((224, 224))
        img.load()
        
        return True
    except Exception as e:
        print(f"❌ Corrupted: {image_path}")
        print(f"   Error: {e}")
        return False


def scan_and_clean_dataset(data_dir, remove_corrupted=False, create_backup=True):
    """
    Scan dataset for corrupted images
    
    Args:
        data_dir: Root data directory (e.g., 'data/train')
        remove_corrupted: If True, delete corrupted images
        create_backup: If True, move corrupted to backup folder instead of deleting
    """
    print("=" * 60)
    print("Image Dataset Checker")
    print("=" * 60)
    print(f"\nScanning: {data_dir}")
    print(f"Remove corrupted: {remove_corrupted}")
    print(f"Create backup: {create_backup}")
    print("\n" + "=" * 60 + "\n")
    
    # Create backup directory if needed
    if remove_corrupted and create_backup:
        backup_dir = os.path.join(os.path.dirname(data_dir), 'corrupted_backups')
        os.makedirs(backup_dir, exist_ok=True)
        print(f"📁 Backup directory: {backup_dir}\n")
    
    total_images = 0
    corrupted_images = []
    
    # Scan all images
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                total_images += 1
                image_path = os.path.join(root, file)
                
                if not check_image(image_path):
                    corrupted_images.append(image_path)
                    
                    # Handle corrupted image
                    if remove_corrupted:
                        if create_backup:
                            # Move to backup
                            rel_path = os.path.relpath(image_path, data_dir)
                            backup_path = os.path.join(backup_dir, rel_path)
                            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                            shutil.move(image_path, backup_path)
                            print(f"   Moved to: {backup_path}")
                        else:
                            # Delete
                            os.remove(image_path)
                            print(f"   Deleted")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total images scanned: {total_images}")
    print(f"Corrupted images found: {len(corrupted_images)}")
    print(f"Clean images: {total_images - len(corrupted_images)}")
    
    if corrupted_images:
        print(f"\n✅ Dataset cleaned! Ready for training.")
        if not remove_corrupted:
            print("\n⚠️  Corrupted images were NOT removed.")
            print("To remove them, run with --remove flag:")
            print("python clean_dataset.py --remove")
    else:
        print(f"\n✅ No corrupted images found! Dataset is clean.")
    
    print("=" * 60)
    
    return corrupted_images


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Check and clean image dataset')
    parser.add_argument('--data-dir', default='data/train', help='Data directory to scan')
    parser.add_argument('--remove', action='store_true', help='Remove corrupted images')
    parser.add_argument('--no-backup', action='store_true', help='Delete instead of backing up')
    
    args = parser.parse_args()
    
    # Also check validation directory
    scan_and_clean_dataset(args.data_dir, args.remove, not args.no_backup)
    
    # Check validation dir if train was cleaned
    if 'train' in args.data_dir:
        val_dir = args.data_dir.replace('train', 'val')
        if os.path.exists(val_dir):
            print("\n\nChecking validation directory...\n")
            scan_and_clean_dataset(val_dir, args.remove, not args.no_backup)
