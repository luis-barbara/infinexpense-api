const API_BASE_URL = "http://localhost:8000"; 

/**
 * Handle all API requests with error handling.
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
        if (response.status === 204) {
            return null;
        }
        try {
            return await response.json();
        } catch (e) {
            return null; 
        }
    }

    
    let errorDetail = "An unknown error occurred.";
    try {
        const errorData = await response.json();
        if (errorData && errorData.detail) {
            errorDetail = errorData.detail;
        } else {
            errorDetail = `Error ${response.status}: ${response.statusText}`;
        }
    } catch (e) {
        errorDetail = `Error ${response.status}: ${response.statusText}`;
    }
    
    throw new Error(errorDetail);
}



/**
 * Get all receipts with filters and pagination.
 */
export async function getReceipts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/receipts/?${query}` : "/receipts/";
    return _handleApiRequest(endpoint);
}

/**
 * Create a new receipt.
 */
export async function createReceipt(data) {
    return _handleApiRequest("/receipts/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

/**
 * Delete a receipt.
 */
export async function deleteReceipt(id) {
    return _handleApiRequest(`/receipts/${id}`, { method: "DELETE" });
}



/**
 * Get receipt by ID.
 */
export async function getReceiptById(id) {
    return _handleApiRequest(`/receipts/${id}`);
}

/**
 * Get products in a receipt.
 */
export async function getReceiptProducts(id) {
    return _handleApiRequest(`/receipts/${id}/products`);
}

/**
 * Get receipt by barcode.
 */
export async function getReceiptByBarcode(barcode) {
    return _handleApiRequest(`/receipts/barcode/${barcode}`);
}

/**
 * Get receipts by merchant.
 */
export async function getReceiptsByMerchant(id, params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/receipts/merchant/${id}?${query}` : `/receipts/merchant/${id}`;
    return _handleApiRequest(endpoint);
}

/**
 * Update a receipt.
 */
export async function updateReceipt(id, data) {
    return _handleApiRequest(`/receipts/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

/**
 * Update products for a receipt
 */
export async function updateReceiptProducts(id, products) {
    return _handleApiRequest(`/receipts/${id}/products`, {
        method: "PUT",
        body: JSON.stringify({ products }),
    });
}