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
**Goal:** Suggest a market price based on pet metadata (Breed, Age, Weight, Health, etc.).

**Architecture:**
- **Type:** Deep Neural Network (MLP - Multi-Layer Perceptron).
- **Inputs:** 7 Metadata Features (Type, Breed, Age, Weight, Health Status, Vaccinated, Country).
- **Layers:** 
  - Input Layer (7 features)
  - Dense(128) + BatchNormalization + Dropout
  - Dense(64) + BatchNormalization + Dropout
  - Dense(32)
  - Output(1) -> Linear Activation (Price)
- **Why Metadata Only?** We found that visual features (the image) are redundant for pricing once the breed is identified. Pricing is driven by market factors (age, health, pedigree/country) rather than the specific pixel arrangement of the photo.

### C. "Model Surgery" (Incremental Learning)
**The Challenge:** Adding a new breed (class) to a trained neural network usually requires retraining from scratch, which is slow and expensive.

**Our Solution:**
1.  **Load** the existing model.
2.  **Remove** the top output layer (e.g., 45 neurons).
3.  **Create** a new output layer with $N+1$ neurons (46 neurons).
4.  **Copy** the weights for the original 45 classes.
5.  **Initialize** the new neuron's weights.
6.  **Train** only the new layer briefly to "settle" it.

---

## 5. Technical Q&A (Interview Prep)

**Q1: Why did you choose MongoDB over SQL?**
> **A:** Pet products vary wildly. A fish has "water_type" while a dog has "breed_size". MongoDB's flexible schema allows us to store these different attributes without complex join tables or sparse columns.

**Q2: How do you handle long-running training tasks?**
> **A:** We use FastAPI's `BackgroundTasks`. When a user starts training, the request returns immediately with a "Started" status, while the heavy Python script runs in a separate process. The frontend polls a status endpoint to update the console log.

**Q3: Why use `GlobalAveragePooling2D` instead of `Flatten`?**
> **A:** `Flatten` keeps all spatial information, leading to a massive number of parameters and overfitting. `GlobalAveragePooling` summarizes the feature map into a single vector, making the model more robust to the *position* of the pet in the image.

**Q4: How do you prevent the model from forgetting old breeds when adding a new one?**
> **A:** We use a **Rehearsal Strategy**. When fine-tuning or adding a breed, we include data from *all* existing breeds in the training batches, not just the new one. This forces the model to maintain its performance on the old tasks while learning the new one.

**Q5: What is the "Confidence Score"?**
> **A:** It's the highest value from the Softmax output layer. Softmax turns the model's raw numbers (logits) into probabilities that sum to 100%.

---

## 6. Directory Structure
- `/frontend`: Next.js Application
- `/backend`: FastAPI Server
- `/ml`: Machine Learning Scripts
    - `data/`: Training images (ignored in git)
    - `models/`: Saved `.keras` files
    - `train.py`: Full retraining script
    - `fine_tune.py`: Accuracy improvement script
    - `add_breed.py`: Model surgery script
    - `train_price_model.py`: Metadata-based price predictor
    - `generate_price_dataset.py`: Synthetic data generator

