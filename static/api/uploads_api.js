// frontend/api/uploads_api.js

const API_BASE_URL = "http://localhost:8000";

/**
 * Upload de foto para um produto da lista-mestra
 * @param {number} productListId - ID do produto
 * @param {File} file - Ficheiro selecionado
 */
export async function uploadProductPhoto(productListId, file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/uploads/product-list/${productListId}/photo`, {
        method: "POST",
        body: formData, // multipart/form-data
    });

    if (!response.ok) {
        let errorMessage = `Erro ${response.status}: ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) errorMessage = errorData.detail;
        } catch {}
        throw new Error(errorMessage);
    }

    return response.json();
}
