const API_BASE_URL = "http://localhost:8000";

/**
 * Upload a photo for a product.
 */
export async function uploadProductPhoto(productListId, file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/uploads/product-list/${productListId}/photo`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) errorMessage = errorData.detail;
        } catch {}
        throw new Error(errorMessage);
    }

    return response.json();
}

/**
 * Upload a photo for a receipt.
 */
export async function uploadReceiptPhoto(receiptId, file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/uploads/receipt/${receiptId}/photo`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) errorMessage = errorData.detail;
        } catch {}
        throw new Error(errorMessage);
    }

    return response.json();
}
