# Frontend Context Documentation

The `frontend/context` directory contains React Context Providers. These providers manage global state that needs to be accessible throughout the application, avoiding the need to pass props down through multiple layers of components (prop drilling).

## 1. `auth-context.tsx` (Authentication Context)

**Role:** Manages the global authentication state of the user.

**Key Features:**
- **State Management**:
    - `user`: Stores the current user's profile information (ID, email, name, role).
    - `token`: Stores the JWT access token used for API requests.
    - `isAuthenticated`: A boolean derived from the user state to quickly check if a user is logged in.
    - `isLoading`: Tracks whether the app is currently checking for an existing session (essential for preventing premature redirects).

- **Persistence**:
    - On application load (`useEffect`), it checks `localStorage` for an existing token.
    - If a token is found, it verifies it by calling the `/auth/me` endpoint via `api.getMe()`.

- **Actions**:
    - `login(token, user)`: Saves the token to local storage, updates state, and redirects the user to the Dashboard.
    - `logout()`: Clears the token from local storage, resets state, and redirects the user to the Login page.

**System Flow Integration:**
1.  **Initialization**: When the app starts (in `layout.tsx`), the `AuthProvider` wraps the entire application.
2.  **Session Check**: It immediately checks if the user was previously logged in.
3.  **Route Protection**: The `AuthGuard` component (in `components/`) consumes this context. If `isLoading` is false and `isAuthenticated` is false, it blocks access to protected pages.
4.  **API Requests**: The `token` stored here is often used by the API utility (in `lib/api.ts`) to attach the `Authorization: Bearer ...` header to outgoing requests.
