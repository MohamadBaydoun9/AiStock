# Services Directory Documentation

The `backend/app/services` directory contains the **business logic** layer of the application. These services act as intermediaries between the API routes (controllers) and the database. They handle data processing, validation rules, and complex operations, keeping the API routes clean and focused on HTTP concerns.

## 1. `auth_service.py` (Authentication Service)
**Role:** Manages user identity, registration, and login verification.

**Key Responsibilities:**
- **User Registration (`create_user`)**:
    - Checks if an email is already registered.
    - Hashes the user's password using bcrypt before storage.
    - Creates the user document in the database with a default or specified role.
- **User Authentication (`authenticate_user`)**:
    - Verifies email and password credentials.
    - Returns the user object if credentials are valid, or `None` otherwise.

## 2. `product_service.py` (Product Service)
**Role:** The core service for managing the pet inventory. It handles the creation, retrieval, updating, and deletion of product listings.

**Key Responsibilities:**
- **Creation (`create_product`)**:
    - Handles the storage of the product image (as binary data).
    - Saves the product metadata (name, price, breed, etc.) to MongoDB.
- **Public Shop Listing (`get_published_products`)**:
    - Retrieves products for the public-facing shop.
    - Implements complex filtering logic:
        - **By Type/Category** (e.g., Dog, Cat).
        - **By Breed** (Regex search).
        - **By Price Range** (Checks both `price_modified` and `price_predicted`).
- **Admin Listing (`get_products`)**:
    - Retrieves a paginated list of products for the admin dashboard.
- **Updates & Deletion**:
    - `update_product`: Modifies existing product details.
    - `delete_product`: Removes a product from the inventory.
- **Image Handling**:
    - `get_product_image`: Retrieves the raw image bytes for a specific product.

## 3. `product_type_service.py` (Product Type Service)
**Role:** Manages the categories (types) of pets available in the store (e.g., "Dog", "Cat", "Fish").

**Key Responsibilities:**
- **Listing (`get_all_types`)**:
    - Returns all product types.
    - **Dynamic Counting**: Calculates and returns the number of products currently assigned to each type (e.g., "Dog (12 items)").
- **Creation (`create_type`)**:
    - Adds a new category, ensuring no duplicates exist.
- **Updates (`update_type`)**:
    - Renames a category.
    - **Cascading Update**: Automatically updates all products that belong to this category to reflect the new name.
- **Deletion (`delete_type`)**:
    - Removes a category.
    - **Safety Check**: Prevents deletion if there are still products assigned to this category to maintain data integrity.

## 4. `stats_service.py` (Statistics Service)
**Role:** Generates analytical data for the Admin Dashboard.

**Key Responsibilities:**
- **Aggregation (`get_summary`)**:
    - Uses a MongoDB Aggregation Pipeline to calculate high-level metrics in a single database query:
        - **Total Products**: Number of unique listings.
        - **Total Items**: Sum of `quantity` across all products.
        - **Total Inventory Value**: Calculates the total monetary value of the stock (`quantity * price`). It intelligently uses `price_modified` if set, falling back to `price_predicted`.
