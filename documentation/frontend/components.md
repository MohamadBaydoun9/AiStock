# Frontend Components Documentation

This directory contains the reusable React components that build the user interface of the SmartStock AI application. These components are designed to be modular, accessible, and consistent with the application's design system.

## 1. Core Components

### `auth-guard.tsx`
**Role:** Route Protection Wrapper.
- **Functionality**: This component wraps pages that require authentication. It checks the user's login status using the `AuthContext`.
- **Flow**:
    - If the user is **loading**, it displays a spinner.
    - If the user is **not authenticated**, it automatically redirects them to the `/login` page.
    - If the user is **authenticated**, it renders the protected content (children).
- **Usage**: Used in `layout.tsx` or specific page wrappers to secure admin and dashboard routes.

### `navbar.tsx`
**Role:** Main Navigation Bar.
- **Functionality**: Provides the top-level navigation for the application.
- **Features**:
    - **Logo**: Links back to the dashboard.
    - **Responsive Links**: Provides quick access to key features:
        - **Upload Item**: For adding new pet inventory.
        - **Dashboard**: The main analytics and list view.
        - **Manage Types**: Admin settings for pet categories.
        - **Train Model**: Interface for the ML "Model Surgery" feature.
    - **Active State**: Highlights the current page button based on the URL path.

### `theme-provider.tsx`
**Role:** Theme Management Context.
- **Functionality**: Wraps the application to provide theme support (Light/Dark mode).
- **Tech Stack**: Built on top of `next-themes`.
- **Usage**: Allows the entire app to switch themes dynamically without page reloads.

## 2. UI Library (`ui/`)
This directory contains the **Atomic Design** building blocks of the application. These components are built using **Shadcn/UI** and **Tailwind CSS**, ensuring a premium, accessible, and consistent look and feel.

**Key Components include:**
- **`button.tsx`**: Standardized buttons with variants (default, ghost, destructive, outline).
- **`card.tsx`**: Container components for grouping content (used heavily in the Dashboard).
- **`input.tsx` & `form.tsx`**: Form controls with built-in validation styling.
- **`dialog.tsx`**: Modal windows for alerts and confirmations.
- **`table.tsx`**: Data grids for displaying inventory lists.
- **`toast.tsx`**: Notification popups for success/error messages.

**Design Philosophy:**
These components are "headless" (powered by Radix UI) but styled with Tailwind, giving us full control over the aesthetics while maintaining high accessibility standards (keyboard navigation, screen reader support).
