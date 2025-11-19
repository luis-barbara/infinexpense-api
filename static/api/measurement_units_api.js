// frontend/api/measurement_units_api.js

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
    
    return response.json();
}

/**
 * Get all measurement units
 * endpoint: GET /measurement-units/
 */
export async function getMeasurementUnits(params = {}) {
    const validParams = {
        skip: params.skip || 0,
        limit: Math.min(params.limit || 100, 1000)
    };
    
    const queryString = new URLSearchParams(validParams).toString();
    const endpoint = queryString ? `/measurement-units/?${queryString}` : '/measurement-units/';
    return _handleApiRequest(endpoint);
}

/**
 * Get a specific measurement unit by ID
 * endpoint: GET /measurement-units/{unit_id}
 */
export async function getMeasurementUnitById(id) {
    return _handleApiRequest(`/measurement-units/${id}`);
}

/**
 * Create a new measurement unit
 * endpoint: POST /measurement-units/
 */
export async function createMeasurementUnit(data) {
    return _handleApiRequest('/measurement-units/', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Update a measurement unit
 * endpoint: PUT /measurement-units/{unit_id}
 */
export async function updateMeasurementUnit(id, data) {
    return _handleApiRequest(`/measurement-units/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

/**
 * Delete a measurement unit
 * endpoint: DELETE /measurement-units/{unit_id}
 */
export async function deleteMeasurementUnit(id) {
    return _handleApiRequest(`/measurement-units/${id}`, {
        method: "DELETE"
    });
}
