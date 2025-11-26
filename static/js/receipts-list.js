import { getReceipts, deleteReceipt } from '/static/api/receipts_api.js';

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
        console.error('Error loading receipts:', error);
        document.getElementById('receiptsList').innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-error);">Error loading receipts: ${error.message}</div>`;
    }
}

/**
 * Render receipts to the DOM
 */
function renderReceipts(receipts) {
    const container = document.getElementById('receiptsList');
    container.innerHTML = '';

    if (receipts.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--text-muted);">No receipts found.</div>';
        document.getElementById('resultsCount').textContent = '0 receipts';
        return;
    }

    receipts.forEach(receipt => {
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT');
        const receiptId = receipt.id;
        
        const row = document.createElement('div');
        row.className = 'receipts-grid animate-slide-up';
        row.setAttribute('data-receipt-id', receiptId);
        row.setAttribute('data-barcode', receipt.barcode || `RCPT-${receiptId}`);
        row.setAttribute('data-merchant', receipt.merchant?.name || 'N/A');
        row.setAttribute('data-date', receipt.purchase_date);
        row.setAttribute('data-products', receipt.products?.length || 0);
        row.setAttribute('data-total', receipt.total_price || 0);

        row.innerHTML = `
            <div><span>RCPT-${receipt.barcode || `RCPT-${receiptId}`}</span></div>
            <div><span>${receipt.merchant?.name || 'N/A'}</span></div>
            <div><span>${receiptDate}</span></div>
            <div><span>${receipt.products?.length || 0} items</span></div>
            <div><span>${(receipt.total_price || 0).toFixed(2)} €</span></div>
            <div style="display: flex; gap: 0.5rem;">
                <a href="view.html?id=${receiptId}" class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.875rem;" title="View">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                    </svg>
                </a>
                <a href="edit.html?id=${receiptId}" class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.875rem;" title="Edit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
                    </svg>
                </a>
                <button class="btn btn-danger" style="padding: 0.4rem 0.8rem; font-size: 0.875rem;" title="Delete" onclick="confirmDelete(${receiptId})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        <line x1="10" y1="11" x2="10" y2="17"/>
                        <line x1="14" y1="11" x2="14" y2="17"/>
                    </svg>
                </button>
            </div>
        `;

        container.appendChild(row);
    });

    document.getElementById('resultsCount').textContent = `${receipts.length} receipt${receipts.length !== 1 ? 's' : ''}`;
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
function sortReceipts(field) {
    const container = document.getElementById('receiptsList');
    const items = Array.from(container.querySelectorAll('.receipts-grid'));
    
    const direction = sortDirection[field] === 'asc' ? 'desc' : 'asc';
    sortDirection[field] = direction;
    
    items.sort((a, b) => {
        let aValue = a.getAttribute(`data-${field}`);
        let bValue = b.getAttribute(`data-${field}`);
        
        if (!aValue || !bValue) return 0;
        
        // Convert to numbers for numeric fields
        if (field === 'products' || field === 'total') {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        }
        
        if (direction === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // Clear and re-append sorted items
    container.innerHTML = '';
    items.forEach(item => container.appendChild(item));
}

/**
 * Delete receipt with confirmation
 */
async function confirmDelete(receiptId) {
    if (!confirm('Are you sure you want to delete this receipt?')) return;

    try {
        console.log('Deleting receipt:', receiptId);
        await deleteReceipt(receiptId);
        console.log('Receipt deleted successfully');
        alert('Receipt deleted successfully!');
        loadReceipts();
    } catch (error) {
        console.error('Error deleting receipt:', error);
        alert('Error deleting receipt: ' + error.message);
    }
}


// Expose to global scope
window.filterItems = filterItems;
window.sortReceipts = sortReceipts;
window.confirmDelete = confirmDelete;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadReceipts();

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', filterItems);
    }
});
