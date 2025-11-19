// frontend/api/products_api.js

const API_BASE_URL = "http://localhost:8000";

/**
 * Helper function for all API requests
 */
async function _handleApiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('Making request to:', url);
    
    const response = await fetch(url, options);
    
    if (!response.ok) {
        let errorDetail = `API Error: ${response.status}`;
        try {
            const error = await response.json();
            console.error('API Error Response:', error);
            errorDetail = error.detail || JSON.stringify(error);
        } catch (e) {
            console.error('Could not parse error response');
        }
        throw new Error(errorDetail);
    }
    
    // Handle 204 No Content (empty response)
    if (response.status === 204) {
        return null;
    }
    
    return response.json();
}

/**
 * Get all products
 * endpoint: GET /products/
 */
export async function getProducts(params = {}) {
    // Use valid parameters - limit max is 1000
    const validParams = {
        skip: params.skip || 0,
        limit: Math.min(params.limit || 100, 1000)  // Cap at 1000
    };
    
    const queryString = new URLSearchParams(validParams).toString();
    const endpoint = queryString ? `/products/?${queryString}` : '/products/';
    return _handleApiRequest(endpoint);
}

/**
 * Get a specific product by ID
 * endpoint: GET /products/{product_id}
 */
export async function getProductById(id) {
    return _handleApiRequest(`/products/${id}`);
}

/**
 * Get product by barcode
 * endpoint: GET /products/barcode/{barcode}
 */
export async function getProductByBarcode(barcode) {
    return _handleApiRequest(`/products/barcode/${barcode}`);
}

/**
 * Get product by name
 * endpoint: GET /products/name/{name}
 */
export async function getProductByName(name) {
    return _handleApiRequest(`/products/name/${name}`);
}

/**
 * Create a new product
 * endpoint: POST /products/
 */
export async function createProduct(data) {
    return _handleApiRequest('/products/', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Update a product
 * endpoint: PUT /products/{product_id}
 */
export async function updateProduct(id, data) {
    return _handleApiRequest(`/products/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Delete a product
 * endpoint: DELETE /products/{product_id}
 */
export async function deleteProduct(id) {
    return _handleApiRequest(`/products/${id}`, {
        method: "DELETE"
    });
}
