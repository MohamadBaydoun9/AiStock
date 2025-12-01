# Frontend Hooks Documentation

The `frontend/hooks` directory contains custom React hooks that encapsulate reusable logic and state management, keeping components clean and focused on UI rendering.

## 1. `use-mobile.ts` (Mobile Detection)

**Role:** Responsive Design Helper.

**Functionality:**
- **Breakpoint Detection**: Listens to the window's resize events to determine if the current viewport width is below a specific breakpoint (default: 768px).
- **State Management**: Returns a boolean `isMobile` that is `true` when the device is considered mobile (width < 768px) and `false` otherwise.
- **Event Listener**: Efficiently adds and removes the `change` event listener on the media query to prevent memory leaks.

**System Flow Integration:**
- **Responsive UI**: Used by components like the `Sidebar` or `Navbar` to conditionally render mobile-specific layouts (e.g., a hamburger menu instead of a full sidebar) or to adjust styles dynamically.

## 2. `use-toast.ts` (Toast Notification System)

**Role:** Global Notification Manager.

**Functionality:**
- **State Management**: Uses a reducer pattern (`reducer`) to manage the list of active toasts. It handles actions like `ADD_TOAST`, `UPDATE_TOAST`, `DISMISS_TOAST`, and `REMOVE_TOAST`.
- **Queue System**: Maintains a queue of toasts, enforcing a limit (default: 1) to prevent flooding the user's screen.
- **Auto-Dismissal**: Handles the timing for automatically removing toasts after a delay (or user interaction).
- **Global Access**: The `toast` function is exported directly, allowing it to be imported and used anywhere, even outside of React components (though typically used within the hook).

**System Flow Integration:**
- **User Feedback**: This is the primary mechanism for providing feedback to the user.
    - **Success**: "Product created successfully."
    - **Error**: "Failed to upload image."
- **Usage**:
    - Imported in components (e.g., `UploadForm`) via `const { toast } = useToast()`.
    - Triggered after API calls (in `lib/api.ts` or component handlers) to inform the user of the operation's result.
    - The `Toaster` component (in `components/ui/toaster.tsx`) consumes the state from this hook to actually render the toast UI on the screen.
