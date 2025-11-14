// frontend/api/products_api.js

const API_BASE_URL = "http://localhost:8000";

/**
 * Função auxiliar para todas as requisições
 */
async function _handleApiRequest(endpoint, options = {}) {
    const config = {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.ok) {
        if (response.status === 204) return null;
        try {
            return await response.json();
        } catch {
            return null;
        }
    }

    let errorDetail = `Erro ${response.status}: ${response.statusText}`;
    try {
        const errorData = await response.json();
        if (errorData && errorData.detail) errorDetail = errorData.detail;
    } catch {}

    throw new Error(errorDetail);
}

// CRUD Products

// Create
export async function createProduct(data) {
    return _handleApiRequest("/products/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

// Read All com filtros
export async function getProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/products/?${query}` : "/products/";
    return _handleApiRequest(endpoint);
}

// Read by ID
export async function getProductById(id) {
    return _handleApiRequest(`/products/${id}`);
}

// Read by Barcode
export async function getProductByBarcode(barcode) {
    return _handleApiRequest(`/products/barcode/${barcode}`);
}

// Read by Name
export async function getProductByName(name) {
    return _handleApiRequest(`/products/name/${name}`);
}

// Update
export async function updateProduct(id, data) {
    return _handleApiRequest(`/products/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

// Delete
export async function deleteProduct(id) {
    return _handleApiRequest(`/products/${id}`, { method: "DELETE" });
}
