import { getMerchantById, deleteMerchant } from '/static/api/merchants_api.js';
import { getReceiptsByMerchant } from '/static/api/receipts_api.js';

let currentMerchantId = null;
let currentMerchant = null;

/**
 * Get merchant ID from URL
 */
function getMerchantIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Load merchant details from API
 */
async function loadMerchant() {
    try {
        currentMerchantId = getMerchantIdFromUrl();
        if (!currentMerchantId) {
            alert('Merchant ID not provided');
            window.location.href = '/static/merchant/list.html';
            return;
        }

        currentMerchant = await getMerchantById(currentMerchantId);
        populateMerchant(currentMerchant);
        
        // Load recent receipts
        await loadRecentReceipts();
    } catch (error) {
        console.error('Erro ao carregar comerciante:', error);
        alert('Erro ao carregar comerciante: ' + error.message);
        window.location.href = '/static/merchant/list.html';
    }
}

/**
 * Populate merchant details
 */
function populateMerchant(merchant) {
    // Set title in header
    const titleEl = document.querySelector('h1.gradient-text');
    if (titleEl) {
        titleEl.textContent = merchant.name;
    }
    
    // Set edit button link
    const editBtn = document.querySelector('a[href*="edit"]');
    if (editBtn) {
        editBtn.href = `/static/merchant/edit.html?id=${merchant.id}`;
    }
    
    // Location - find by the location div class
    const locationValueEl = document.querySelector('div.location');
    if (locationValueEl) {
        locationValueEl.textContent = merchant.location || '-';
        console.log('Set location to:', merchant.location);
    }
    
    // Notes - Handle missing notes field
    const notesP = document.getElementById('merchant-notes');
    if (notesP) {
        const notesText = merchant.notes || merchant.description || 'No notes available.';
        notesP.textContent = notesText;
    }
    
    console.log('Full merchant object:', merchant);
}

/**
 * Load recent receipts for merchant
 */
async function loadRecentReceipts() {
    try {
        const receipts = await getReceiptsByMerchant(currentMerchantId);
        renderReceipts(receipts);
    } catch (error) {
        console.error('Error loading receipts:', error);
    }
}

/**
 * Render receipts list
 */
function renderReceipts(receipts) {
    const container = document.querySelector('.list-container');
    if (!container) {
        console.error('Container not found');
        return;
    }
    container.innerHTML = '';
    
    // Update receipts title with count
    const receiptsTitle = document.getElementById('receipts-title');
    if (receiptsTitle) {
        receiptsTitle.textContent = `🧾 Recent Receipts (${receipts.length})`;
        console.log('Updated receipts title to:', receipts.length);
    }
    
    // Update Total Receipts - find all font-semibold text-lg divs and update the second one
    const allInfoDivs = document.querySelectorAll('.font-semibold.text-lg');
    if (allInfoDivs.length >= 2) {
        allInfoDivs[1].textContent = `${receipts.length} receipt${receipts.length !== 1 ? 's' : ''}`;
        console.log('Set total receipts to:', receipts.length);
    }
    
    // Update Last Visit - update the third info div
    if (receipts.length > 0) {
        const sortedReceipts = [...receipts].sort((a, b) => new Date(b.purchase_date) - new Date(a.purchase_date));
        const lastReceipt = sortedReceipts[0];
        const lastVisitDate = new Date(lastReceipt.purchase_date).toLocaleDateString('pt-PT', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        if (allInfoDivs.length >= 3) {
            allInfoDivs[2].textContent = lastVisitDate;
            console.log('Set last visit to:', lastVisitDate);
        }
    }
    
    if (receipts.length === 0) {
        container.innerHTML = '<div style="padding: 1rem; text-align: center;">No receipts found</div>';
        return;
    }
    
    // Sort receipts by date (newest first)
    receipts.sort((a, b) => new Date(b.purchase_date) - new Date(a.purchase_date));
    
    receipts.forEach(receipt => {
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        const itemCount = receipt.products ? receipt.products.length : 0;
        const total = receipt.total_price || 0;
        
        const item = document.createElement('div');
        item.style.display = 'grid';
        item.style.gridTemplateColumns = '2fr 1.5fr 1fr 1fr';
        item.style.gap = '1rem';
        item.style.padding = '1rem';
        item.style.borderBottom = '1px solid hsl(var(--border) / 0.2)';
        item.style.alignItems = 'center';
        
        item.innerHTML = `
            <a href="/static/receipt/view.html?id=${receipt.id}" style="color: hsl(var(--primary)); text-decoration: none; font-weight: 500;">${receipt.barcode || `RCPT-${receipt.id}`}</a>
            <div>${receiptDate}</div>
            <div>${itemCount} item${itemCount !== 1 ? 's' : ''}</div>
            <div style="font-weight: 600; color: hsl(var(--primary));">${total.toFixed(2)} €</div>
        `;
        
        container.appendChild(item);
    });
}

/**
 * Delete merchant with confirmation
 */
async function deleteMerchantConfirm() {
    if (!confirm('Are you sure you want to delete this merchant?')) return;

    try {
        await deleteMerchant(currentMerchantId);
        alert('Comerciante eliminado com sucesso!');
        window.location.href = '/static/merchant/list.html';
    } catch (error) {
        console.error('Error deleting merchant:', error);
        alert('Error deleting merchant: ' + error.message);
    }
}

// Expose to global scope
window.deleteMerchantConfirm = deleteMerchantConfirm;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchant();
});