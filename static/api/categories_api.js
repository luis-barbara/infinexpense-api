const API_BASE_URL = "";  // Use relative URLs

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
    
    return response.json();
}

/**
 * Get all categories with optional date filtering.
 */
export async function getCategories(params = {}) {
    const validParams = {
        skip: params.skip || 0,
        limit: Math.min(params.limit || 100, 1000)
    };
    
    // Add optional date parameters
    if (params.start_date) {
        validParams.start_date = params.start_date;
    }
    if (params.end_date) {
        validParams.end_date = params.end_date;
    }
    
    const queryString = new URLSearchParams(validParams).toString();
    const endpoint = queryString ? `/categories/?${queryString}` : '/categories/';
    return _handleApiRequest(endpoint);
}

/**
 * Get a specific category by ID
 * endpoint: GET /categories/{category_id}
 */
export async function getCategoryById(id) {
    return _handleApiRequest(`/categories/${id}`);
}

/**
 * Create a new category
 * endpoint: POST /categories/
 */
export async function createCategory(categoryData) {
    return await _handleApiRequest('/categories/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(categoryData)
    });
}

/**
 * Update a category
 * endpoint: PUT /categories/{id}
 */
export async function updateCategory(id, categoryData) {
    return await _handleApiRequest(`/categories/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(categoryData)
    });
}

/**
 * Delete a category
 * endpoint: DELETE /categories/{id}
 */
export async function deleteCategory(id) {
    const response = await fetch(`${API_BASE_URL}/categories/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error || `HTTP error! status: ${response.status}`);
    }

    // 204 No Content returns nothing - don't try to parse JSON
    if (response.status === 204) {
        return { success: true };
    }

    return await response.json();
}
