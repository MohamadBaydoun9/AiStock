# Frontend App Directory Documentation

The `frontend/app` directory is the core of the Next.js 14 application, utilizing the **App Router** for file-system-based routing.

## 1. Global Layout & Styles

### `layout.tsx` (Root Layout)
**Role:** The top-level wrapper for the entire application.
**Functionality:**
- **Providers**: Wraps the app in the `AuthProvider` to make session state globally available.
- **Global UI**: Renders the `Navbar` (top navigation) and `Toaster` (notification container) so they persist across page transitions.
- **Fonts**: Loads and applies the `Geist` font family.
- **Metadata**: Defines global SEO metadata (title, description, icons).

### `globals.css`
**Role:** Global Stylesheet.
**Functionality:**
- **Tailwind Directives**: Imports Tailwind CSS layers.
- **Theme Variables**: Defines CSS variables for the color palette (using OKLCH for vibrant, accessible colors) for both Light and Dark modes.
- **Base Styles**: Sets default background and text colors.

### `page.tsx` (Root Page)
**Role:** The landing page (`/`).
**Functionality:**
- Currently serves as a redirector, immediately sending users to `/dashboard`.

### `not-found.tsx`
**Role:** 404 Error Page.
**Functionality:**
- Displays a user-friendly "Page Not Found" message with a button to return home.

## 2. Route Structure (Pages)

The directory structure directly maps to the URL paths:

- **`/login`**: User login page.
- **`/register`**: User registration page.
- **`/dashboard`**: The main hub for authenticated users, displaying statistics and the product list.
- **`/upload`**: The interface for uploading new pet images and adding products.
- **`/shop`**: The public-facing storefront view.
- **`/products/[id]`**: Dynamic route for viewing details of a specific product.
- **`/settings/product-types`**: Admin interface for managing pet categories.
- **`/admin/train`**: Admin interface for the "Model Surgery" (training) feature.

## 3. System Flow Integration

1.  **Request**: A user visits `smartstock.ai/dashboard`.
2.  **Routing**: Next.js matches the URL to `app/dashboard/page.tsx`.
3.  **Layout**: The request passes through `app/layout.tsx`.
    - `AuthProvider` checks for a session.
    - `Navbar` is rendered.
4.  **Page Rendering**: `app/dashboard/page.tsx` is rendered.
    - It likely uses `AuthGuard` (from `components/`) to verify the user is logged in.
    - It fetches data using `api.getStats()` and `api.getProducts()` (from `lib/api.ts`).
5.  **Interaction**: User clicks "Upload".
    - `Navbar` handles the client-side navigation to `/upload`.
    - The `layout.tsx` remains mounted (no full page reload), only the page content swaps.
