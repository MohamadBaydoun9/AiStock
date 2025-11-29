"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { User, api } from "@/lib/api";
import { useRouter } from "next/navigation";

interface AuthContextType {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (token: string, user: User) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            setToken(storedToken);
            // Fetch user info using the token
            api.getMe()
                .then((userData) => {
                    setUser(userData);
                })
                .catch(() => {
                    // If token is invalid, logout
                    logout();
                })
                .finally(() => {
                    setIsLoading(false);
                });
        } else {
            setIsLoading(false);
        }
    }, []);

    const login = (newToken: string, newUser: User) => {
        localStorage.setItem("token", newToken);
        setToken(newToken);
        setUser(newUser);
        router.push("/dashboard");
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
        router.push("/login");
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                isAuthenticated: !!user,
                isLoading,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
