# Pet Breed Classification Model

Complete ML pipeline for classifying pet breeds using transfer learning with MobileNetV3.

## 🎯 Features

- **Pet Type Classification**: Dog or Cat
- **Breed Identification**: Specific breed within pet type
- **Price Prediction**: Estimated price based on breed
- **Transfer Learning**: Using pre-trained MobileNetV3-Small
- **Data Augmentation**: Comprehensive augmentation for robustness
- **Two-Phase Training**: Initial training + fine-tuning
- **FastAPI Integration**: Automatic backend integration

## 📁 Dataset Structure

Organize your images in the following structure:

```
ml/data/
├── train/
│   ├── Dog/
│   │   ├── Golden_Retriever/
│   │   │   ├── dog1.jpg
│   │   │   ├── dog2.jpg
│   │   │   └── ... (50-100 images recommended)
│   │   ├── Labrador/
│   │   │   ├── lab1.jpg
│   │   │   └── ...
│   │   ├── German_Shepherd/
│   │   ├── Bulldog/
│   │   └── ... (add more breeds)
│   └── Cat/
│       ├── Persian/
│       │   ├── cat1.jpg
│       │   └── ...
│       ├──  Siamese/
│       ├── Maine_Coon/
│       └── ... (add more breeds)
└── val/
    └── (same structure as train, with 20% of your images)
```

### Important Notes:

1. **Folder Names**: Use underscores for breed names (e.g., `Golden_Retriever`)
2. **Image Format**: JPG, PNG supported
3. **Image Quality**: Clear, well-lit photos work best
4. **Quantity**: Minimum 50 images per breed recommended
5. **Validation Split**: Put 20% of your data in the `val` folder
6. **Consistent Structure**: Both train and val must have identical folder structures

### Example Breeds You Can Add:

**Dogs:**
- Golden_Retriever
- Labrador
- German_Shepherd
- Bulldog
- Poodle
- Husky
- Beagle
- Corgi
- Chihuahua
- Rottweiler

**Cats:**
- Persian
- Siamese
- Maine_Coon
- Bengal
- Ragdoll
- British_Shorthair
- Sphynx
- Scottish_Fold
- Abyssinian
- Russian_Blue

## 🚀 Training the Model

### Step 1: Install Dependencies

```bash
cd ml
pip install -r requirements.txt
```

### Step 2: Prepare Your Dataset

1. Create the folder structure as shown above
2. Add your training images to `ml/data/train/`
3. Add validation images to `ml/data/val/`

### Step 3: Run Training

```bash
cd ml
python train.py
```

The training process will:
1. **Phase 1**: Train classification head (50 epochs)
2. **Phase 2**: Fine-tune entire model (20 epochs)
3. Save best model to `ml/models/pet_classifier.h5`
4. Save class mapping to `ml/models/class_mapping.json`

### Step 4: Monitor Training

Watch for:
- Training accuracy
- Validation accuracy
- Loss values
- Early stopping (if validation stops improving)

Training typically takes:
- CPU: 2-4 hours
- GPU: 20-40 minutes

## 🧪 Testing Predictions

Test your model on a single image:

```bash
cd ml
python predict.py path/to/your/test/image.jpg
```

Output example:
```
==================================================
Prediction Results
==================================================
Pet Type: Dog
Breed: Golden Retriever
Predicted Price: $1500.00
Confidence: 95.23%

Top 3 Predictions:
1. Golden Retriever: 95.23%
2. Labrador: 3.45%
3. Friendly Dog: 1.12%
```

## 🔌 Backend Integration

The model automatically integrates with your FastAPI backend:

1. After training completes, restart your backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. The `/ml/classify-and-predict` endpoint will now use your trained model

3. If the model isn't found, it falls back to stub responses

## ⚙️ Configuration

Edit `config.py` to customize:

- **Image size**: Default 224x224
- **Batch size**: Default 32
- **Learning rates**: Initial and fine-tuning
- **Augmentation parameters**: Rotation, zoom, brightness
- **Breed prices**: Add/modify prices for breeds

## 📊 Model Architecture

**Base Model**: MobileNetV3-Small
- Parameters: ~2.5M
- Input: 224x224x3 RGB images
- Pre-trained on ImageNet

**Custom Head**:
- Global Average Pooling
- Dense(256) + Dropout(0.3) + BatchNorm
- Dense(128) + Dropout(0.3) + BatchNorm  
- Dense(num_classes) with Softmax

**Data Augmentation**:
- Random rotation (±15°)
- Horizontal flip
- Random zoom (90-110%)
- Brightness adjustment
- Color jittering
- Random shifts

## 🎓 Training Strategy

1. **Transfer Learning**: Start with ImageNet weights
2. **Freeze Base**: Initially freeze MobileNetV3 layers
3. **Train Head**: Train only custom classification layers
4. **Fine-Tune**: Unfreeze last 30 layers and fine-tune
5. **Callbacks**:
   - Model checkpointing (save best)
   - Early stopping (patience: 5 epochs)
   - Learning rate reduction (patience: 3 epochs)

## 📈 Expected Performance

With sufficient data (50+ images per breed):
- **Top-1 Accuracy**: 85-95%
- **Top-3 Accuracy**: 95-99%
- **Inference Time**: <100ms on CPU, <10ms on GPU

## 🐛 Troubleshooting

**Error: Data directory not found**
- Ensure you created `ml/data/train/` and `ml/data/val/`
- Check folder structure matches documentation

**Low accuracy**
- Add more training images (aim for 100+ per breed)
- Check image quality (clear, well-lit photos)
- Ensure consistent image quality across breeds
- Try increasing epochs

**Out of memory**
- Reduce batch size in `config.py`
- Use smaller image size (reduce `IMG_SIZE`)

**Model not loading in backend**
- Check model exists at `ml/models/pet_classifier.h5`
- Restart backend after training
- Check backend console for errors

## 📝 Files Created During Training

After training, you'll find:
- `ml/models/pet_classifier.h5` - Trained model
- `ml/models/class_mapping.json` - Class names and mapping
- `ml/models/training_history.json` - Training metrics
- `logs/` - TensorBoard logs

## 🔍 Viewing Training Progress

Use TensorBoard to visualize training:

```bash
cd ml
tensorboard --logdir logs
```

Then open `http://localhost:6006` in your browser.

## 📚 Next Steps

1. Collect pet images for your chosen breeds
2. Organize images in the required structure
3. Run training
4. Test predictions
5. Integrate with frontend upload flow

Happy training! 🐕🐈
