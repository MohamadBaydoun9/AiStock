from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from typing import Optional
import shutil
import os
import zipfile
import subprocess
import sys

router = APIRouter()

# Base path for ML data
# Current file: backend/app/api/routes_train.py
# We need to go up 4 levels to reach project root: api -> app -> backend -> project_root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ML_DIR = os.path.join(BASE_DIR, "ml")
TRAIN_DIR = os.path.join(ML_DIR, "data", "train")
VAL_DIR = os.path.join(ML_DIR, "data", "val")

def run_training_script(script_name: str):
    """
    Runs the python training script in a subprocess
    """
    script_path = os.path.join(ML_DIR, script_name)
    
    # Use the same python interpreter as the running process
    python_executable = sys.executable
    
    # Ensure logs directory exists
    os.makedirs(os.path.join(ML_DIR, "logs"), exist_ok=True)
    
    # Run in background
    with open(os.path.join(ML_DIR, "logs", "training.log"), "a", encoding="utf-8") as log_file:
        subprocess.Popen(
            [python_executable, script_path],
            cwd=ML_DIR,
            stdout=log_file,
            stderr=log_file
        )

@router.post("/add-breed")
async def add_new_breed(
    background_tasks: BackgroundTasks,
    breed_name: str = Form(...),
    product_type: str = Form(...),
    images_zip: UploadFile = File(...)
):
    """
    Uploads a zip of images for a new breed and triggers model training.
    """
    # 1. Validate inputs
    if not images_zip.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP archive")
    
    # Normalize names
    breed_name = breed_name.strip()
    product_type = product_type.strip() # e.g., "Dog", "Cat"
    
    # 2. Prepare directories
    train_target_dir = os.path.join(TRAIN_DIR, product_type, breed_name)
    val_target_dir = os.path.join(VAL_DIR, product_type, breed_name)
    
    if os.path.exists(train_target_dir):
        # If breed exists, we are just adding more data -> Fine Tuning
        mode = "fine_tune"
    else:
        # New breed -> Model Surgery
        mode = "add_breed"
        os.makedirs(train_target_dir, exist_ok=True)
        os.makedirs(val_target_dir, exist_ok=True)
        
    # 3. Save and Extract Zip
    zip_path = os.path.join(ML_DIR, "zips", f"{breed_name}.zip")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(images_zip.file, buffer)
        
    # Extract to a temp folder first
    temp_extract_dir = os.path.join(ML_DIR, "temp_extract", breed_name)
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    os.makedirs(temp_extract_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)
            
        # 4. Distribute Images (80% Train, 20% Val)
        import random
        
        # Find all images recursively in temp folder
        all_images = []
        for root, dirs, files in os.walk(temp_extract_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_images.append(os.path.join(root, file))
        
        if not all_images:
            raise HTTPException(status_code=400, detail="No images found in ZIP file")
            
        random.shuffle(all_images)
        split_idx = int(len(all_images) * 0.8)
        train_images = all_images[:split_idx]
        val_images = all_images[split_idx:]
        
        # Move files
        for img_path in train_images:
            shutil.move(img_path, os.path.join(train_target_dir, os.path.basename(img_path)))
            
        for img_path in val_images:
            shutil.move(img_path, os.path.join(val_target_dir, os.path.basename(img_path)))
            
        # Cleanup temp
        shutil.rmtree(temp_extract_dir)
        
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")
    except Exception as e:
        # Cleanup on error
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")
        
    # 5. Trigger Training in Background
    if mode == "add_breed":
        background_tasks.add_task(run_training_script, "add_breed.py")
        message = f"New breed '{breed_name}' added ({len(train_images)} train, {len(val_images)} val). Model training started in background."
    else:
        background_tasks.add_task(run_training_script, "fine_tune.py")
        message = f"Images added to existing breed '{breed_name}' ({len(train_images)} train, {len(val_images)} val). Fine-tuning started."
        
    return {
        "status": "success",
        "message": message,
        "mode": mode,
        "breed": breed_name,
        "type": product_type
    }

@router.get("/status")
async def get_training_status():
    """
    Check if a training process is running
    """
    # Simple check: see if python process with our script is running
    # This is a basic implementation. For production, use Redis/Celery.
    # For now, we can check the log file's last modification time or lock file.
    
    log_file = os.path.join(ML_DIR, "logs", "training.log")
    if not os.path.exists(log_file):
        return {"status": "idle", "logs": []}
        
    # Read last 50 lines of log
    try:
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            # Efficiently read last N lines
            lines = f.readlines()
            last_lines = lines[-50:] if lines else []
            
        # Determine status based on last log line
        status = "running"
        if last_lines:
            last_line = last_lines[-1].strip()
            # Check for various completion messages
            if ("Training Complete" in last_line or 
                "Fine-Tuning Complete" in last_line or 
                "SUCCESS: New breed added" in last_line or
                "Error" in last_line):
                status = "completed"
            elif "Epoch" in last_line:
                status = "training"
                
        return {
            "status": status,
            "logs": [line.strip() for line in last_lines]
        }
    except Exception as e:
        return {"status": "error", "logs": [str(e)]}
@router.get("/breeds/{product_type}")
async def get_existing_breeds(product_type: str):
    """
    List all existing breeds for a given product type
    """
    type_dir = os.path.join(TRAIN_DIR, product_type)
    if not os.path.exists(type_dir):
        return {"breeds": []}
        
    breeds = []
    for item in os.listdir(type_dir):
        if os.path.isdir(os.path.join(type_dir, item)):
            breeds.append(item)
            
    return {"breeds": sorted(breeds)}

@router.get("/all-breeds")
async def get_all_breeds():
    """
    List all existing breeds grouped by product type
    """
    all_breeds = {}
    
    if not os.path.exists(TRAIN_DIR):
        return all_breeds
        
    for product_type in os.listdir(TRAIN_DIR):
        type_dir = os.path.join(TRAIN_DIR, product_type)
        if os.path.isdir(type_dir):
            breeds = []
            for item in os.listdir(type_dir):
                if os.path.isdir(os.path.join(type_dir, item)):
                    breeds.append(item)
            all_breeds[product_type] = sorted(breeds)
            
    return all_breeds
