// static/api/receipts_api.js



const API_BASE_URL = "http://localhost:8000"; 

/**
 * Função auxiliar para TODAS as requisições
 * @param {string} endpoint endpoint da API 
 * @param {object} options opções do 'fetch' 
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

    // Gestão de Erros 
    if (response.ok) {
        // Se for um '204 No Content' (como o Delete), não há JSON para ler, devolve 'null'
        if (response.status === 204) {
            return null;
        }
        // Tenta ler o JSON (pode falhar se o body estiver vazio)
        try {
            return await response.json();
        } catch (e) {
            return null; 
        }
    }

    
    let errorDetail = "Ocorreu um erro desconhecido.";
    try {
        // Tenta ler o JSON de erro do FastAPI (ex: {"detail": "Receipt not found"})
        const errorData = await response.json();
        if (errorData && errorData.detail) {
            errorDetail = errorData.detail;
        } else {
            errorDetail = `Erro ${response.status}: ${response.statusText}`;
        }
    } catch (e) {
        // Se o erro nao for JSON
        errorDetail = `Erro ${response.status}: ${response.statusText}`;
    }
    
    throw new Error(errorDetail);
}



/**
 * Obtém a lista de recibos, com todos os filtros do router.
 * endpoint: GET /receipts/
 */
export async function getReceipts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/receipts/?${query}` : "/receipts/";
    return _handleApiRequest(endpoint);
}

/**
 * Cria um novo recibo.
 * endpoint: POST /receipts/
 */
export async function createReceipt(data) {
    return _handleApiRequest("/receipts/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

/**
 * Apaga um recibo.
 * endpoint: DELETE /receipts/{receipt_id}
 */
export async function deleteReceipt(id) {
    return _handleApiRequest(`/receipts/${id}`, { method: "DELETE" });
}



/**
 * Obtém um recibo específico pelo ID.
 * endpoint: GET /receipts/{receipt_id}
 */
export async function getReceiptById(id) {
    return _handleApiRequest(`/receipts/${id}`);
}

/**
 * Obtém os produtos de um recibo.
 * endpoint: GET /receipts/{receipt_id}/products
 */
export async function getReceiptProducts(id) {
    return _handleApiRequest(`/receipts/${id}/products`);
}

/**
 * Obtém um recibo pelo barcode.
 * endpoint: GET /receipts/barcode/{barcode}
 */
export async function getReceiptByBarcode(barcode) {
    return _handleApiRequest(`/receipts/barcode/${barcode}`);
}

/**
 * Obtém recibos de um supermercado.
 * endpoint: GET /receipts/merchant/{merchant_id}
 */
export async function getReceiptsByMerchant(id, params = {}) {
    // router tem 'skip' e 'limit' neste endpoint
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/receipts/merchant/${id}?${query}` : `/receipts/merchant/${id}`;
    return _handleApiRequest(endpoint);
}

/**
 * Atualiza um recibo.
 * endpoint: PUT /receipts/{receipt_id}
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