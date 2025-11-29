const API_URL = "http://localhost:8000";

export interface User {
    user_id: string;
    email: string;
    full_name?: string;
    role: string;
    created_at: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user: User;
}

export interface Product {
    _id: string;
    product_id: string;
    product_name: string;
    product_type: string;
    price_predicted: number;
    price_modified?: number | null;
    quantity: number;
    date_added: string;
    has_image: boolean;
    published: boolean;
    // Metadata fields
    age_months?: number;
    weight_kg?: number;
    health_status?: number;
    vaccinated?: boolean;
    country?: string;
    predicted_breed?: string;
    prediction_confidence?: number;
}

export interface StatsSummary {
    total_products: number;
    total_items: number;
    total_value: number;
}

export interface MLResponse {
    product_type: string;
    product_name: string;
    price_predicted: number;
    confidence: number;
    exists: boolean;
    existing_product?: any;
}

export interface ProductType {
    type_id: string;
    name: string;
    created_at: string;
    product_count: number;
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
    const token = localStorage.getItem("token");
    const headers = {
        ...options.headers,
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    } as HeadersInit;

    const response = await fetch(`${API_URL}${url}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Handle unauthorized (e.g., logout)
        localStorage.removeItem("token");
        window.location.href = "/login";
    }

    return response;
}

export const api = {
    // Auth
    async register(data: any): Promise<User> {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error("Registration failed");
        return response.json();
    },

    async login(data: any): Promise<AuthResponse> {
        const formData = new URLSearchParams();
        formData.append("username", data.email);
        formData.append("password", data.password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData.toString(),
        });
        if (!response.ok) throw new Error("Login failed");
        return response.json();
    },

    async getMe(): Promise<User> {
        const response = await fetchWithAuth("/auth/me");
        if (!response.ok) throw new Error("Failed to fetch user");
        return response.json();
    },

    // Products
    async getProducts(params?: { search?: string; type?: string }): Promise<Product[]> {
        const query = new URLSearchParams(params as any).toString();
        const response = await fetchWithAuth(`/products?${query}`);
        if (!response.ok) throw new Error("Failed to fetch products");
        return response.json();
    },

    async getProduct(id: string): Promise<Product> {
        const response = await fetchWithAuth(`/products/${id}`);
        if (!response.ok) throw new Error("Failed to fetch product");
        return response.json();
    },

    async createProduct(formData: FormData): Promise<Product> {
        const response = await fetchWithAuth("/products/", {
            method: "POST",
            body: formData,
        });
        if (!response.ok) throw new Error("Failed to create product");
        return response.json();
    },

    // Stats
    async getStats(): Promise<StatsSummary> {
        const response = await fetchWithAuth("/stats/summary");
        if (!response.ok) throw new Error("Failed to fetch stats");
        return response.json();
    },

    // ML Stub
    async classifyImage(formData: FormData): Promise<MLResponse> {
        const response = await fetch(`${API_URL}/ml/classify-and-predict`, {
            method: "POST",
            body: formData,
        });
        if (!response.ok) throw new Error("AI classification failed");
        return response.json();
    },

    // Product Types
    async getProductTypes(): Promise<ProductType[]> {
        const response = await fetch(`${API_URL}/product-types/`);
        if (!response.ok) throw new Error("Failed to fetch product types");
        return response.json();
    },

    async createProductType(name: string): Promise<ProductType> {
        const response = await fetchWithAuth("/product-types", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });
        if (!response.ok) throw new Error("Failed to create product type");
        return response.json();
    },

    async updateProductType(type_id: string, name: string): Promise<ProductType> {
        const response = await fetchWithAuth(`/product-types/${type_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });
        if (!response.ok) throw new Error("Failed to update product type");
        return response.json();
    },

    async deleteProductType(type_id: string): Promise<void> {
        const response = await fetchWithAuth(`/product-types/${type_id}`, {
            method: "DELETE",
        });
        if (!response.ok) throw new Error("Failed to delete product type");
    }
};
