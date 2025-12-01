# API Directory Structure & File Roles

This document explains the role and responsibility of each file within the `backend/app/api` directory. These files define the HTTP endpoints (routes) and dependencies for the FastAPI application.

## 1. `deps.py` (Dependencies)
**Role:** Contains reusable dependencies for dependency injection in FastAPI routes.
**Key Functions:**
- `get_current_user`: Validates the JWT token and retrieves the current user from the database. Used to protect routes that require authentication.
- `get_current_admin`: Verifies if the authenticated user has the "admin" role. Used to protect sensitive routes (e.g., deleting products, training models).

## 2. `routes_auth.py` (Authentication Routes)
**Role:** Handles user authentication and authorization.
**Endpoints:**
- `POST /register`: Registers a new user.
- `POST /login`: Authenticates a user and returns a JWT access token.
- `GET /me`: Returns the profile of the currently authenticated user.

## 3. `routes_ml_stub.py` (ML Classification Interface)
**Role:** Acts as the interface between the API and the Machine Learning image classification model.
**Key Features:**
- Dynamically loads ML modules (`predict.py`, `config.py`) from the `ml/` directory.
- **Endpoint** `POST /classify-and-predict`: Accepts an image file, runs it through the classification model, and returns the predicted breed, product type, and confidence score.
- Includes a fallback mechanism (stub) to return mock data if the ML model fails to load or execute.

## 4. `routes_price.py` (Price Prediction Routes)
**Role:** Handles AI-driven price predictions based on pet metadata.
**Endpoints:**
- `POST /predict-price`: Predicts the market price of a pet based on structured data (breed, age, weight, health, etc.).
- `POST /classify-and-price`: A combined workflow that first classifies the breed from an image and then predicts the price using the classification result and provided metadata.

## 5. `routes_product_types.py` (Product Type Management)
**Role:** Manages the categories/types of pets (e.g., "Dog", "Cat", "Fish").
**Endpoints:**
- `GET /`: Lists all available product types (public).
- `POST /`: Creates a new product type (Admin only).
- `PUT /{type_id}`: Updates an existing product type (Admin only).
- `DELETE /{type_id}`: Deletes a product type (Admin only).

## 6. `routes_products.py` (Product Management)
**Role:** The core CRUD (Create, Read, Update, Delete) interface for pet products.
**Endpoints:**
- `POST /`: Creates a new product listing with an image (User/Admin).
- `GET /`: Lists products with pagination and filtering options.
- `GET /shop/published`: Specialized endpoint for the public shop front, supporting filters like breed, price range, etc.
- `GET /{product_id}`: Retrieves details of a specific product.
- `GET /{product_id}/image`: Serves the product image.
- `PUT /{product_id}`: Updates product details.
- `DELETE /{product_id}`: Removes a product (Admin only).

## 7. `routes_stats.py` (Dashboard Statistics)
**Role:** Provides aggregated data for the admin dashboard.
**Endpoints:**
- `GET /summary`: Returns high-level metrics such as total sales, total products, and other key performance indicators (KPIs).

## 8. `routes_train.py` (Model Training & Management)
**Role:** Manages the "Model Surgery" and fine-tuning processes for the ML models.
**Key Features:**
- Handles background tasks to run long-running training scripts without blocking the API.
- **Endpoints:**
    - `POST /add-breed`: Accepts a ZIP file of images to add a new breed or fine-tune an existing one. Triggers the training script.
    - `GET /status`: Polls the training logs to provide real-time status updates (Running, Completed, Error).
    - `GET /breeds/{product_type}`: Lists all breeds currently known to the model for a specific type.
    - `GET /all-breeds`: Lists all breeds grouped by type.
