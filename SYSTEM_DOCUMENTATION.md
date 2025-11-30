# SmartStock AI - System Documentation

## 1. System Overview
**SmartStock AI** is an intelligent inventory management system for pet shops. It leverages advanced Machine Learning to automate the identification of pet breeds and predict optimal pricing based on market data. The system is built with a modern, scalable tech stack ensuring high performance and a premium user experience.

## 2. Technology Stack

### Frontend
- **Framework:** Next.js 14 (React) - Chosen for server-side rendering (SSR) and SEO benefits.
- **Styling:** Tailwind CSS & Shadcn/UI - For rapid, consistent, and accessible UI development.
- **State Management:** React Hooks & Context API.
- **Icons:** Lucide React.
- **Animations:** CSS Keyframes & Tailwind Animate.

### Backend
- **Framework:** FastAPI (Python) - Selected for its high performance (ASGI) and native support for async ML operations.
- **Database:** MongoDB (Motor) - A NoSQL database chosen for its flexibility in handling varying product attributes (schema-less).
- **Authentication:** JWT (JSON Web Tokens) with OAuth2 password flow.

### Machine Learning (The Core)
- **Library:** TensorFlow & Keras.
- **Base Model:** EfficientNetB0 (Pre-trained on ImageNet).
- **Training:** Custom fine-tuning and incremental learning pipelines.

---

## 3. Key Features

### 🔐 Authentication & Security
- **JWT Auth:** Secure login system with token-based session management.
- **Role-Based Access:** Admin-only routes for training and statistics.

### 📸 Smart Upload & Classification
- **Drag & Drop Interface:** User-friendly image upload.
- **Real-time AI Inference:** Instantly identifies:
    - **Product Type** (Dog, Cat, etc.)
    - **Breed** (e.g., Akita Inu, Persian)
    - **Confidence Score** (%)
    - **Predicted Price** ($)

### 📊 Admin Dashboard & Statistics
- **Sales Analytics:** Visual charts tracking revenue and stock levels.
- **Model Performance:** Tracks MAE (Mean Absolute Error) for price predictions to monitor AI accuracy.
- **Inventory Management:** CRUD operations for pet products.

### 🧠 Dynamic Model Training (Advanced)
- **"Model Surgery":** A custom feature allowing the addition of *new* breeds without retraining from scratch.
- **Background Processing:** Training runs asynchronously to keep the UI responsive.
- **Real-time Console:** Live streaming of training logs to the browser via polling.

---

## 4. AI Architecture Deep Dive

### A. Pet Breed Classification Model
**Goal:** Identify the specific breed of a pet from an image.

**Architecture:**
```python
# Simplified Structure
base_model = EfficientNetB0(include_top=False, weights='imagenet')
base_model.trainable = False # Frozen initially

model = Sequential([
    base_model,
    GlobalAveragePooling2D(), # Reduces spatial dimensions
    BatchNormalization(),     # Stabilizes training
    Dropout(0.2),             # Prevents overfitting
    Dense(num_classes, activation='softmax') # Output layer (Probability distribution)
])
```

**Why EfficientNetB0?**
1.  **Efficiency:** It achieves high accuracy with significantly fewer parameters than ResNet50 or VGG16.
2.  **Speed:** Faster inference time, crucial for a real-time web app.
3.  **Transfer Learning:** We leverage features learned from millions of ImageNet photos, allowing us to train on smaller pet datasets effectively.

**Training Strategy:**
1.  **Phase 1 (Head Training):** We freeze the "Brain" (EfficientNet) and only train the "Classifier" (Top layers).
2.  **Phase 2 (Fine-Tuning):** We unfreeze the top 20 layers of EfficientNet and train with a very low learning rate (`1e-5`) to adapt the model specifically to pet features (fur texture, ear shapes).

### B. Price Prediction Model
**Goal:** Suggest a market price based on breed, age, and type.

**Architecture:**
- **Type:** Regression Model (Random Forest / Linear Regressor logic implemented in custom logic or simple neural net).
- **Inputs:** Breed (One-hot encoded), Age, Weight.
- **Output:** Single continuous value (Price).
- **Metric:** MAE (Mean Absolute Error) - chosen because it's robust to outliers and easy to interpret (e.g., "off by $50").

### C. "Model Surgery" (Incremental Learning)
> **A:** Pet products vary wildly. A fish has "water_type" while a dog has "breed_size". MongoDB's flexible schema allows us to store these different attributes without complex join tables or sparse columns.

**Q2: How do you handle long-running training tasks?**
> **A:** We use FastAPI's `BackgroundTasks`. When a user starts training, the request returns immediately with a "Started" status, while the heavy Python script runs in a separate process. The frontend polls a status endpoint to update the console log.

**Q3: Why use `GlobalAveragePooling2D` instead of `Flatten`?**
> **A:** `Flatten` keeps all spatial information, leading to a massive number of parameters and overfitting. `GlobalAveragePooling` summarizes the feature map into a single vector, making the model more robust to the *position* of the pet in the image.

**Q4: How do you prevent the model from forgetting old breeds when adding a new one?**
> **A:** We use a technique called "Replay" (implicitly) or simply a low learning rate on the shared weights. By initializing the new weights carefully and keeping the existing weights close to their original values, we minimize drift.

**Q5: What is the "Confidence Score"?**
> **A:** It's the highest value from the Softmax output layer. Softmax turns the model's raw numbers (logits) into probabilities that sum to 100%.

---

## 6. Directory Structure
- `/frontend`: Next.js Application
- `/backend`: FastAPI Server
- `/ml`: Machine Learning Scripts
    - `data/`: Training images
    - `models/`: Saved `.keras` files
    - `train.py`: Full retraining script
    - `fine_tune.py`: Accuracy improvement script
    - `add_breed.py`: Model surgery script
