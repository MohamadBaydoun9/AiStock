"""
GPU Detection and Verification Script
"""
import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("=" * 60)
print("GPU Detection for Pet Breed Classifier")
print("=" * 60)

# TensorFlow version
print(f"\n📦 TensorFlow version: {tf.__version__}")

# GPU availability
gpus = tf.config.list_physical_devices('GPU')
print(f"\n🎮 GPU Available: {len(gpus) > 0}")

if gpus:
    for i, gpu in enumerate(gpus):
        print(f"\n✅ GPU {i}: {gpu.name}")
        
        # Get GPU details
        gpu_details = tf.config.experimental.get_device_details(gpu)
        if gpu_details:
            print(f"   Device Name: {gpu_details.get('device_name', 'Unknown')}")
        
        # Check memory
        try:
            # Set memory growth
            tf.config.experimental.set_memory_growth(gpu, True)
            print(f"   Memory growth enabled")
        except RuntimeError as e:
            print(f"   Note: {e}")
    
    print("\n" + "=" * 60)
    print("🚀 GPU Training Enabled!")
    print("=" * 60)
    print("\nExpected training time with RTX 5070:")
    print("  • Full training (30 epochs + 10 fine-tune): 15-20 minutes")
    print("  • Quick mode (20 + 5 epochs): 5-8 minutes")
    print("  • Inference per image: <10ms")
    
else:
    print("\n" + "=" * 60)
    print("⚠️  No GPU Detected - Will use CPU")
    print("=" * 60)
    print("\nTo enable GPU:")
    print("1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
    print("2. Install TensorFlow with GPU: pip install tensorflow[and-cuda]")
    print("3. Restart terminal and run this script again")
    print("\nExpected CPU training time:")
    print("  • Full training: 2-4 hours")
    print("  • Quick mode: 30-45 minutes")

print("\n" + "=" * 60)

# Test computation
print("\n🧪 Testing GPU computation...")
try:
    with tf.device('/GPU:0' if gpus else '/CPU:0'):
        # Simple matrix multiplication
        a = tf.random.normal([1000, 1000])
        b = tf.random.normal([1000, 1000])
        c = tf.matmul(a, b)
    print("✅ Computation test successful!")
except Exception as e:
    print(f"❌ Computation test failed: {e}")

print("=" * 60)
