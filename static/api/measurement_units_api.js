// frontend/api/measurement_units_api.js

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

// CRUD Measurement Units

// Create
export async function createMeasurementUnit(data) {
    return _handleApiRequest("/measurement-units/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

// Read All
export async function getMeasurementUnits(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/measurement-units/?${query}` : "/measurement-units/";
    return _handleApiRequest(endpoint);
}

// Read by ID
export async function getMeasurementUnitById(id) {
    return _handleApiRequest(`/measurement-units/${id}`);
}

// Update
export async function updateMeasurementUnit(id, data) {
    return _handleApiRequest(`/measurement-units/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

// Delete
export async function deleteMeasurementUnit(id) {
    return _handleApiRequest(`/measurement-units/${id}`, { method: "DELETE" });
}
