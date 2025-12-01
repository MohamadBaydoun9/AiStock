# Backend API Documentation

The `backend/app/api` directory contains the route handlers (controllers) for the FastAPI application. Each file corresponds to a specific domain or feature set.

## 1. Core Dependencies (`deps.py`)

**Role:** Shared logic for route protection.

**Key Functions:**
- **`get_current_user`**:
    - Validates the JWT token from the `Authorization` header.
    - Decodes the token to get the `user_id`.
    - Fetches the user from MongoDB.
    - **Usage**: Injected into routes to ensure the user is logged in.
- **`get_current_admin`**:
    - Wraps `get_current_user`.
    - Checks if `user.role == "admin"`.
    - **Usage**: Protects sensitive routes like deleting products or training models.

## 2. Authentication (`routes_auth.py`)

**Role:** User session management.

**Endpoints:**
- `POST /auth/register`: Creates a new user account.
- `POST /auth/login`: Validates credentials and returns a JWT access token.
- `GET /auth/me`: Returns the profile of the currently logged-in user.

## 3. Product Management (`routes_products.py`)

**Role:** Inventory CRUD operations.

**Endpoints:**
- `GET /products/`: List products with pagination and search.
- `GET /products/shop/published`: Public endpoint for the storefront (supports filtering by price, breed, type).
- `POST /products/`: Create a new product (Admin/User). Handles image upload and metadata storage.
- `GET /products/{id}`: Get details of a single product.
- `PUT /products/{id}`: Update product details.
- `DELETE /products/{id}`: Remove a product (Admin only).
- `GET /products/{id}/image`: Serves the product image directly from GridFS/Storage.

## 4. Model Training (`routes_train.py`)

**Role:** Interface for the "Model Surgery" and "Fine-Tuning" features.

**Endpoints:**
- `POST /train/add-breed`:
    - **Input**: `breed_name`, `product_type`, `images_zip`.
    - **Logic**:
        1. Validates and extracts the ZIP file.
        2. Splits images into `train` (80%) and `val` (20%) directories.
        3. Checks if the breed already exists.
        4. Triggers a **Background Task**:
            - If new breed: Runs `ml/add_breed.py`.
            - If existing breed: Runs `ml/fine_tune.py`.
- `GET /train/status`: Reads the training logs to report progress (e.g., "Epoch 1/5").
- `GET /train/all-breeds`: Lists all supported breeds grouped by type.

## 5. Machine Learning (`routes_ml_stub.py`)

**Role:** Image Classification.

**Endpoints:**
- `POST /ml/classify`:
    - **Input**: Image file.
    - **Logic**: Calls the `PetClassifier` (from `ml/predict.py`) to identify the breed.
    - **Output**: Breed name, confidence score, and predicted price.

## 6. Price Prediction (`routes_price.py`)

**Role:** Metadata-based pricing.

**Endpoints:**
- `POST /price/predict`:
    - **Input**: Metadata (Age, Weight, Health, etc.).
    - **Logic**: Calls `predict_price` (from `ml/predict_price.py`).
    - **Output**: Estimated market value in USD.

## 7. System Flow Integration

1.  **Request**: Frontend sends a request (e.g., `POST /products/`).
2.  **Validation**: Pydantic models (in `app/models/`) validate the request body.
3.  **Dependency**: `deps.get_current_user` verifies the token.
4.  **Service Layer**: The route calls `ProductService` (in `app/services/`) to handle business logic.
5.  **Database**: The service interacts with MongoDB (via `app/db/mongo.py`).
6.  **Response**: The route returns a JSON response matching the Pydantic response model.
