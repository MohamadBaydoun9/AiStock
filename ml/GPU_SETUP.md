# GPU Setup for Training

## Enable GPU for TensorFlow

### Step 1: Install CUDA Toolkit and cuDNN

Your RTX 5070 requires:
- CUDA 11.8 or 12.x
- cuDNN 8.6+

**Option A: Install via NVIDIA** (Recommended)
1. Download CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Download cuDNN: https://developer.nvidia.com/cudnn

**Option B: Use conda** (Easier)
```bash
conda install -c conda-forge cudatoolkit=11.8 cudnn=8.6
```

### Step 2: Install TensorFlow with GPU Support

```bash
cd ml
pip install tensorflow[and-cuda]
```

Or for latest version:
```bash
pip install tensorflow==2.15.0
```

TensorFlow 2.10+ includes GPU support automatically if CUDA is detected.

### Step 3: Verify GPU Detection

Run this to check if GPU is detected:

```bash
cd ml
python check_gpu.py
```

You should see:
```
✅ GPU Available: True
GPU Name: NVIDIA GeForce RTX 5070 Laptop GPU
GPU Memory: 8192 MB
```

### Step 4: Train with GPU

Just run training normally - GPU will be used automatically:

```bash
cd ml
python train.py
```

## Expected Performance

**With RTX 5070:**
- Full training: 15-20 minutes (vs 2-4 hours on CPU)
- Quick mode: 5-8 minutes (vs 30-45 min on CPU)
- Inference: <10ms per image (vs 50-100ms on CPU)

## Troubleshooting

### "Could not load dynamic library 'cudart64_110.dll'"
- Install CUDA Toolkit from NVIDIA website
- Restart terminal after installation

### "No GPU detected"
- Update NVIDIA drivers
- Reinstall TensorFlow: `pip install --upgrade tensorflow`
- Check CUDA installation: `nvidia-smi`

### Out of Memory
- Reduce batch size in config.py: `BATCH_SIZE = 16`
- Your RTX 5070 has 8GB VRAM, should handle batch_size=32-64 easily

## GPU Settings (Optional)

For optimal performance, add to start of `train.py`:

```python
# Allow GPU memory growth (prevents TF from using all VRAM)
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
```
