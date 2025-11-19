import { getMerchantById, deleteMerchant } from '../api/merchants_api.js';
import { getReceiptsByMerchant } from '../api/receipts_api.js';

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
            window.location.href = 'list.html';
            return;
        }

        console.log('Loading merchant ID:', currentMerchantId);
        currentMerchant = await getMerchantById(currentMerchantId);
        console.log('Merchant loaded:', currentMerchant);
        
        populateMerchant(currentMerchant);
        
        // Load recent receipts
        await loadRecentReceipts();
    } catch (error) {
        console.error('Erro ao carregar comerciante:', error);
        alert('Erro ao carregar comerciante: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate merchant details
 */
function populateMerchant(merchant) {
    // Set title
    document.querySelector('.page-title').textContent = merchant.name;
    
    // Set edit button link
    document.querySelector('a[href*="edit"]').href = `edit.html?id=${merchant.id}`;
    
    // Set delete button
    document.querySelector('button.btn-danger').onclick = function() {
        deleteMerchantConfirm();
    };
    
    // Location
    const locationEl = document.querySelector('.product-info-grid .product-info-item:nth-child(1) .product-info-value');
    if (locationEl) {
        locationEl.textContent = merchant.location || '-';
        console.log('Set location to:', merchant.location);
    }
    
    // Notes - Handle missing notes field
    const notesP = document.getElementById('merchant-notes');
    if (notesP) {
        const notesText = merchant.notes || merchant.description || 'No notes available.';
        notesP.textContent = notesText;
        console.log('Set notes to:', notesText);
    } else {
        console.warn('Notes paragraph element not found');
    }
    
    // Merchant image
    if (merchant.image_path) {
        const img = document.getElementById('merchant-image');
        img.src = merchant.image_path;
        img.style.display = 'block';
        document.getElementById('no-photo-placeholder').style.display = 'none';
        console.log('Merchant image set');
    }
    
    console.log('Full merchant object:', merchant);
}

/**
 * Load recent receipts for merchant
 */
async function loadRecentReceipts() {
    try {
        const receipts = await getReceiptsByMerchant(currentMerchantId);
        console.log('Receipts loaded:', receipts.length);
        
        renderReceipts(receipts);
    } catch (error) {
        console.error('Erro ao carregar recibos:', error);
    }
}

/**
 * Render receipts list
 */
function renderReceipts(receipts) {
    const container = document.querySelector('.scrollable-list .list-container');
    container.innerHTML = '';
    
    // Update receipts title with count
    const receiptsTitle = document.getElementById('receipts-title');
    if (receiptsTitle) {
        receiptsTitle.textContent = `Recent Receipts (${receipts.length})`;
        console.log('Updated receipts title to:', receipts.length);
    }
    
    // Update total receipts count
    const totalReceiptsEl = document.querySelector('.product-info-grid .product-info-item:nth-child(2) .product-info-value');
    if (totalReceiptsEl) {
        totalReceiptsEl.textContent = `${receipts.length} receipt${receipts.length !== 1 ? 's' : ''}`;
        console.log('Set total receipts to:', receipts.length);
    }
    
    // Update last visit
    if (receipts.length > 0) {
        const lastReceipt = receipts[0];
        const lastVisitDate = new Date(lastReceipt.purchase_date).toLocaleDateString('pt-PT', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        const lastVisitEl = document.querySelector('.product-info-grid .product-info-item:nth-child(3) .product-info-value');
        if (lastVisitEl) {
            lastVisitEl.textContent = lastVisitDate;
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
        item.className = 'list-item';
        item.style.gridTemplateColumns = '2fr 1.5fr 1fr 1fr';
        
        item.innerHTML = `
            <div class="list-item-main" style="grid-template-columns: 2fr 1.5fr 1fr 1fr;">
                <div class="list-item-value"><a href="../receipt/view.html?id=${receipt.id}" class="link-primary">${receipt.barcode || `RCPT-${receipt.id}`}</a></div>
                <div class="list-item-value">${receiptDate}</div>
                <div class="list-item-value">${itemCount} items</div>
                <div class="list-item-value" style="font-weight: 600; color: var(--primary);">${total.toFixed(2)} €</div>
            </div>
        `;
        
        container.appendChild(item);
    });
}

/**
 * Delete merchant with confirmation
 */
async function deleteMerchantConfirm() {
    if (!confirm('Tem a certeza que deseja eliminar este comerciante?')) return;

    try {
        await deleteMerchant(currentMerchantId);
        alert('Comerciante eliminado com sucesso!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Erro ao eliminar comerciante:', error);
        alert('Erro ao eliminar comerciante: ' + error.message);
    }
}

// Expose to global scope
window.deleteMerchantConfirm = deleteMerchantConfirm;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchant();
});