import { getReceipts, deleteReceipt } from '../api/receipts_api.js';

let allReceipts = [];
let sortDirection = {};

/**
 * Load receipts from API and populate the list
 */
async function loadReceipts() {
    try {
        allReceipts = await getReceipts();
        renderReceipts(allReceipts);
    } catch (error) {
        console.error('Erro ao carregar recibos:', error);
        alert('Erro ao carregar recibos: ' + error.message);
    }
}

/**
 * Render receipts to the DOM
 */
function renderReceipts(receipts) {
    const container = document.getElementById('receiptsList');
    container.innerHTML = '';

    if (receipts.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center;">Nenhum recibo encontrado.</div>';
        return;
    }

    receipts.forEach(receipt => {
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT');
        const receiptId = receipt.id;
        
        const item = document.createElement('div');
        item.className = 'list-item receipt-item';
        item.setAttribute('data-receipt-id', receiptId);
        item.setAttribute('data-merchant', receipt.merchant?.name || 'N/A');
        item.setAttribute('data-date', receipt.purchase_date);
        item.setAttribute('data-products', receipt.products?.length || 0);
        item.setAttribute('data-total', receipt.total_price || 0);

        item.innerHTML = `
            <div class="list-item-main receipts-list-grid">
                <div class="list-item-value"><span>RCPT-${receipt.barcode || `RCPT-${receiptId}`}</span></div>
                <div class="list-item-value"><span>${receipt.merchant?.name || 'N/A'}</span></div>
                <div class="list-item-value"><span>${receiptDate}</span></div>
                <div class="list-item-value"><span>${receipt.products?.length || 0} items</span></div>
                <div class="list-item-value"><span>${(receipt.total_price || 0).toFixed(2)} €</span></div>
                <div class="list-item-actions">
                    <a href="view.html?id=${receiptId}" class="btn btn-secondary btn-sm" title="View">👁️</a>
                    <a href="edit.html?id=${receiptId}" class="btn btn-secondary btn-sm" title="Edit">✏️</a>
                    <button class="btn btn-danger btn-sm" title="Delete" onclick="confirmDelete(${receiptId})">🗑️</button>
                </div>
            </div>
        `;

        container.appendChild(item);
    });
}

/**
 * Filter receipts based on search input
 */
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allReceipts.filter(receipt => {
        const merchantName = receipt.merchant?.name || '';
        const barcode = receipt.barcode || '';
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT');
        
        const searchText = `${merchantName} ${barcode} ${receiptDate}`.toLowerCase();
        return searchText.includes(searchTerm);
    });
    renderReceipts(filtered);
}

/**
 * Sort receipts by specified field and direction
 */
function sortReceipts(field, direction) {
    const container = document.getElementById('receiptsList');
    const items = Array.from(container.querySelectorAll('.receipt-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'products' || field === 'spent') {
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
 * Delete receipt with confirmation
 */
async function confirmDelete(receiptId) {
    if (!confirm('Tem a certeza que deseja eliminar este recibo?')) return;

    try {
        console.log('Deleting receipt:', receiptId);
        await deleteReceipt(receiptId);
        console.log('Receipt deleted successfully');
        alert('Recibo eliminado com sucesso!');
        loadReceipts(); // Reload list
    } catch (error) {
        console.error('Erro ao eliminar recibo:', error);
        alert('Erro ao eliminar recibo: ' + error.message);
    }
}

// Expose to global scope
window.filterItems = filterItems;
window.sortReceipts = sortReceipts;
window.confirmDelete = confirmDelete;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadReceipts();
});
