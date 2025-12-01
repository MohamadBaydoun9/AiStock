
import tensorflow as tf
import numpy as np

def verify():
    print("Verifying MobileNetV3 preprocessing...")
    x = np.array([0, 127.5, 255], dtype=np.float32)
    y = tf.keras.applications.mobilenet_v3.preprocess_input(x)
    print(f"Input: {x}")
    print(f"Output: {y}")
    
    if np.allclose(y, [-1, 0, 1], atol=0.1):
        print("✅ preprocess_input expects [0, 255] and maps to [-1, 1]")
    else:
        print("❌ Unexpected behavior")

if __name__ == '__main__':
    verify()
