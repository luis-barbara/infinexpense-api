// static/api/reports_api.js


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

// Reports API 

// 1. Gastos por categoria (Dashboard)
export async function getSpendingByCategory(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/reports/spending-by-category?${query}` : `/reports/spending-by-category`;
    return _handleApiRequest(endpoint);
}

// 2. Report Supermercados (Analytics)
export async function getEnrichedMerchants(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/reports/enriched-merchants?${query}` : `/reports/enriched-merchants`;
    return _handleApiRequest(endpoint);
}

// 3. KPIs do Dashboard
export async function getDashboardKPIs(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/reports/dashboard-kpis?${query}` : `/reports/dashboard-kpis`;
    return _handleApiRequest(endpoint);
}
