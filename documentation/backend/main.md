# Backend Core Documentation

This document provides a detailed overview of the core components of the backend application, including the main entry point, configuration, database connection, data models, and seeding scripts.

## 1. Main Application Entry Point (`main.py`)
**Role:** The heart of the FastAPI application. It initializes the app, configures middleware, and registers all API routes.

**Key Components:**
- **App Initialization**: Creates the `FastAPI` instance with the project title.
- **CORS Middleware**: Configures Cross-Origin Resource Sharing to allow the frontend to communicate with the backend.
- **Database Events**:
    - `startup`: Connects to MongoDB when the server starts.
    - `shutdown`: Closes the MongoDB connection when the server stops.
- **Route Registration**: Includes all routers from the `api` module (Auth, Products, Stats, ML, etc.) with their respective prefixes and tags.
- **Root Endpoint**: A simple health check endpoint (`GET /`) to verify the server is running.

## 2. Core Configuration (`core/`)
This directory handles the application's configuration and security utilities.

### `config.py`
**Role:** Centralizes all application settings using Pydantic's `BaseSettings`.
- **Environment Variables**: Loads settings like `MONGODB_URI`, `JWT_SECRET_KEY`, and `PROJECT_NAME` from environment variables, providing defaults for development.
- **Caching**: Uses `@lru_cache` to load settings once and improve performance.

### `security.py`
**Role:** Provides cryptographic utilities for authentication.
- **Password Hashing**: Uses `bcrypt` to securely hash passwords (`get_password_hash`) and verify them (`verify_password`).
- **JWT Generation**: Creates JSON Web Tokens (`create_access_token`) with an expiration time for secure user sessions.

## 3. Database Layer (`db/`)
### `mongo.py`
**Role:** Manages the asynchronous connection to the MongoDB database.
- **Motor Client**: Uses `motor.motor_asyncio` for non-blocking database operations.
- **Singleton Pattern**: The `MongoDB` class maintains a single client instance (`mongo_db`) used across the application.
- **Dependency**: Exports `get_database` for easy injection into services and routes.

## 4. Data Models (`models/`)
These Pydantic models define the structure and validation rules for data moving in and out of the API.

### `user.py`
- **UserCreate**: Schema for registering a new user (email, password, full name).
- **UserRead**: Schema for returning user profile data (excludes password).
- **UserInDB**: Internal schema representing the user document stored in MongoDB (includes hashed password).

### `product.py`
- **ProductCreate**: Schema for creating a new product listing.
- **ProductRead**: Schema for returning product details to the client.
- **ProductUpdate**: Schema for updating product fields (all fields optional).

### `product_type.py`
- **ProductTypeCreate**: Schema for creating a new pet category.
- **ProductTypeRead**: Schema for returning category details, including the count of associated products.

## 5. Database Seeding (`seeds/`)
### `seed_admin.py`
**Role:** A utility script to initialize the database with a default Admin user.
- **Functionality**:
    - Connects to MongoDB.
    - Checks if an admin user already exists.
    - If not, creates a new admin with default credentials (`admin@smartstock.com` / `Admin123!`).
- **Usage**: Run via `python -m app.seeds.seed_admin`.
