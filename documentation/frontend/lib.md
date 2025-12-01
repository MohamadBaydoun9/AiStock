# Frontend Library Documentation

The `frontend/lib` directory contains utility functions, type definitions, and the API client layer. This separation of concerns ensures that components remain focused on UI rendering while complex logic and data fetching are handled centrally.

## 1. `api.ts` (API Client)

**Role:** The bridge between the Frontend and the Backend API.

**Key Features:**
- **Centralized Configuration**: Defines the `API_URL` (e.g., `http://localhost:8000`) in one place.
- **Type Definitions**: Exports TypeScript interfaces for API responses (`User`, `Product`, `AuthResponse`, `MLResponse`, `StatsSummary`) to ensure type safety across the app.
- **Authentication Wrapper (`fetchWithAuth`)**:
    - Automatically retrieves the JWT token from `localStorage`.
    - Attaches the `Authorization: Bearer <token>` header to requests.
    - Handles `401 Unauthorized` responses by redirecting the user to the login page.
- **API Methods**:
    - **Auth**: `login`, `register`, `getMe`.
    - **Products**: `getProducts` (with search/filter), `getProduct`, `createProduct`.
    - **Stats**: `getStats` for the dashboard.
    - **ML**: `classifyImage` for the AI prediction feature.
    - **Product Types**: CRUD operations for managing pet categories.

**System Flow Integration:**
- **Data Fetching**: Components (like `DashboardPage`) call `api.getProducts()` inside `useEffect` hooks.
- **Actions**: Forms (like `UploadForm`) call `api.createProduct()` on submission.
- **Context**: The `AuthContext` uses `api.login()` and `api.getMe()` to manage user sessions.

## 2. `utils.ts` (Utilities)

**Role:** General helper functions.

**Key Functions:**
- **`cn` (Classname Merger)**:
    - Combines `clsx` (for conditional classes) and `tailwind-merge` (to resolve conflicting Tailwind classes).
    - **Usage**: Essential for building reusable UI components where custom classes might override default styles.
    - *Example*: `<Button className={cn("bg-blue-500", className)} />` ensures `bg-red-500` passed in `className` correctly overrides the default blue.

## 3. `types.ts` (Global Types)

**Role:** Shared TypeScript definitions.

**Key Definitions:**
- **`Product`**: Defines the shape of a product object used in UI components.
- **`ClassificationResult`**: Defines the structure of the data returned by the ML model (breed, confidence, price).

**Note**: There is some overlap between types defined here and in `api.ts`. `api.ts` types generally reflect the raw backend response, while `types.ts` might contain types more specific to frontend component props or state.
