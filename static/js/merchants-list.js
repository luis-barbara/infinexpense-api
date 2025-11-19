import { getMerchants, deleteMerchant } from '../api/merchants_api.js';
import { getReceipts } from '../api/receipts_api.js';

let allMerchants = [];
let sortDirection = {};

/**
 * Load merchants from API and calculate statistics
 */
async function loadMerchants() {
    try {
        const merchants = await getMerchants();
        const receipts = await getReceipts({ limit: 1000 });

        // Calculate receipts and total spent per merchant
        allMerchants = merchants.map(merchant => {
            const merchantReceipts = receipts.filter(r => r.merchant_id === merchant.id);
            const totalSpent = merchantReceipts.reduce((sum, r) => sum + parseFloat(r.total_price || 0), 0);
            
            return {
                ...merchant,
                receiptCount: merchantReceipts.length,
                totalSpent: totalSpent
            };
        });

        renderMerchants(allMerchants);
    } catch (error) {
        console.error('Erro ao carregar comerciantes:', error);
    }
}

/**
 * Render merchants to the DOM
 */
function renderMerchants(merchants) {
    const container = document.getElementById('merchantsList');
    container.innerHTML = '';

    if (merchants.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center;">Nenhum comerciante encontrado.</div>';
        return;
    }

    merchants.forEach(merchant => {
        const item = document.createElement('div');
        item.className = 'list-item merchant-item';
        
        const name = (merchant.name || '').toLowerCase();
        
        item.setAttribute('data-name', name);
        item.setAttribute('data-receipts', merchant.receiptCount);
        item.setAttribute('data-total', merchant.totalSpent);

        item.innerHTML = `
            <div class="list-item-main merchants-list-grid">
                <div class="list-item-value"><span>${merchant.name}</span></div>
                <div class="list-item-value"><span>${merchant.location || 'N/A'}</span></div>
                <div class="list-item-value"><span>${merchant.receiptCount} receipts</span></div>
                <div class="list-item-value"><span>${merchant.totalSpent.toFixed(2)} €</span></div>
                <div class="list-item-actions">
                    <a href="view.html?id=${merchant.id}" class="btn btn-secondary btn-sm" title="View">👁️</a>
                    <a href="edit.html?id=${merchant.id}" class="btn btn-secondary btn-sm" title="Edit">✏️</a>
                    <button class="btn btn-danger btn-sm" title="Delete" onclick="confirmDelete(${merchant.id})">🗑️</button>
                </div>
            </div>
        `;

        container.appendChild(item);
    });
}

/**
 * Filter merchants by name
 */
function filterItems() {
    const searchInput = document.getElementById('searchInput');
    
    if (!searchInput) {
        console.warn('Search input not found');
        return;
    }
    
    const searchTerm = searchInput.value.toLowerCase().trim();
    const allItems = document.querySelectorAll('.merchant-item');

    allItems.forEach(item => {
        const name = item.getAttribute('data-name') || '';
        const matches = name.includes(searchTerm) || searchTerm === '';
        item.style.display = matches ? 'flex' : 'none';
    });
}

/**
 * Sort merchants by specified field and direction
 */
function sortMerchants(field, direction) {
    const container = document.getElementById('merchantsList');
    const items = Array.from(container.querySelectorAll('.merchant-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'receipts' || field === 'total') {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        }
        
        if (direction === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // Re-append sorted items to container
    items.forEach(item => container.appendChild(item));
}

/**
 * Delete merchant with confirmation
 */
async function confirmDelete(merchantId) {
    if (!confirm('Tem a certeza que deseja eliminar este comerciante?')) return;

    try {
        await deleteMerchant(merchantId);
        alert('Comerciante eliminado com sucesso!');
        loadMerchants(); // Reload list
    } catch (error) {
        console.error('Erro ao eliminar comerciante:', error);
        alert('Erro ao eliminar comerciante: ' + error.message);
    }
}

// Expose to global scope
window.filterItems = filterItems;
window.sortMerchants = sortMerchants;
window.confirmDelete = confirmDelete;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchants();
    
    // Add search input listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', filterItems);
    }
});
