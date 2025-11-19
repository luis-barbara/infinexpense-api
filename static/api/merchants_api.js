// src/static/js/merchants_api.js

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
    
    // Handle 204 No Content
    if (response.status === 204) {
        return null;
    }
    
    return response.json();
}

/**
 * Get all merchants
 */
export async function getMerchants(params = {}) {
    const validParams = {
        skip: params.skip || 0,
        limit: Math.min(params.limit || 100, 1000)
    };
    
    const queryString = new URLSearchParams(validParams).toString();
    const endpoint = queryString ? `/merchants/?${queryString}` : '/merchants/';
    return _handleApiRequest(endpoint);
}

/**
 * Get merchant by ID
 */
export async function getMerchantById(id) {
    return _handleApiRequest(`/merchants/${id}`);
}

/**
 * Create a new merchant
 */
export async function createMerchant(data) {
    return _handleApiRequest('/merchants/', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Update a merchant
 */
export async function updateMerchant(id, data) {
    return _handleApiRequest(`/merchants/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Delete a merchant
 */
export async function deleteMerchant(id) {
    return _handleApiRequest(`/merchants/${id}`, {
        method: "DELETE"
    });
}

/**
 * Upload merchant photo
 */
export async function uploadMerchantPhoto(id, file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return _handleApiRequest(`/merchants/${id}/upload-photo`, {
        method: "POST",
        body: formData
    });
}
