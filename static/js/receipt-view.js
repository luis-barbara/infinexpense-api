import { getReceiptById, deleteReceipt } from '../api/receipts_api.js';

let currentReceiptId = null;
let currentReceipt = null;

/**
 * Get receipt ID from URL
 */
function getReceiptIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Load receipt details from API
 */
async function loadReceipt() {
    try {
        currentReceiptId = getReceiptIdFromUrl();
        if (!currentReceiptId) {
            alert('Receipt ID not provided');
            window.location.href = 'list.html';
            return;
        }

        const { getReceiptById } = await import('../api/receipts_api.js');
        currentReceipt = await getReceiptById(currentReceiptId);
        
        populateReceipt(currentReceipt);
    } catch (error) {
        console.error('Erro ao carregar recibo:', error);
        alert('Erro ao carregar recibo: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate receipt details
 */
function populateReceipt(receipt) {
    // Set title
    document.getElementById('receipt-title').textContent = 
        `Receipt: ${receipt.barcode || `RCPT-${receipt.id}`}`;
    
    // Set edit button link
    document.getElementById('edit-btn').href = `edit.html?id=${receipt.id}`;
    
    // Merchant info
    const merchantLink = document.getElementById('merchant-link');
    merchantLink.textContent = receipt.merchant?.name || 'Unknown';
    merchantLink.href = `../merchant/view.html?id=${receipt.merchant_id}`;
    
    document.getElementById('merchant-location').textContent = 
        receipt.merchant?.location || '-';
    
    // Date & Time
    const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('receipt-datetime').textContent = receiptDate;
    
    // Total
    document.getElementById('receipt-total').textContent = 
        `${(receipt.total_price || 0).toFixed(2)} €`;
    
    // Notes
    if (receipt.notes) {
        const notesSection = document.getElementById('notes-section');
        const notesField = document.getElementById('receipt-notes');
        notesField.textContent = receipt.notes;
        notesSection.style.display = 'block';
    }
    
    // Products
    renderProducts(receipt.products || []);
    
    // Image
    if (receipt.receipt_photo) {
        const img = document.getElementById('receipt-image');
        const container = document.getElementById('receipt-image-container');
        img.src = receipt.receipt_photo;
        container.style.display = 'block';
        document.getElementById('no-photo-placeholder').style.display = 'none';
    }
}

/**
 * Render products list
 */
function renderProducts(products) {
    const container = document.getElementById('products-list');
    container.innerHTML = '';
    
    // Update items count
    document.getElementById('items-title').textContent = `Item List (${products.length})`;
    
    if (products.length === 0) {
        container.innerHTML = '<div style="padding: 1rem; text-align: center;">No items</div>';
        return;
    }

    // Add product rows
    products.forEach((product) => {
        const item = document.createElement('div');
        item.className = 'products-table-grid';
        
        const price = parseFloat(product.price) || 0;
        const quantity = parseFloat(product.quantity) || 0;
        
        item.innerHTML = `
            <div>${product.product_list?.name || '-'}</div>
            <div>${product.product_list?.category?.name || '-'}</div>
            <div style="text-align: right;">${quantity.toFixed(2)}</div>
            <div style="text-align: right;">${price.toFixed(2)} €</div>
            <div style="text-align: right;">${(quantity*price).toFixed(2)} €</div>
        `;
        
        container.appendChild(item);
    });
}

/**
 * Sort products by field and direction
 */
function sortProducts(field, direction) {
    const container = document.getElementById('products-list');
    const items = Array.from(container.querySelectorAll('.list-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'quantity' || field === 'price') {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        }
        
        if (direction === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // Re-append sorted items
    items.forEach(item => container.appendChild(item));
}

/**
 * Delete receipt with confirmation
 */
async function deleteCurrentReceipt() {
    if (!confirm('Tem a certeza que deseja eliminar este recibo?')) return;

    try {
        const { deleteReceipt } = await import('../api/receipts_api.js');
        await deleteReceipt(currentReceiptId);
        alert('Recibo eliminado com sucesso!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Erro ao eliminar recibo:', error);
        alert('Erro ao eliminar recibo: ' + error.message);
    }
}

// Expose to global scope
window.sortProducts = sortProducts;
window.deleteCurrentReceipt = deleteCurrentReceipt;

/**
 * Open image modal to view zoomed photo
 */
function openImageModal() {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const receiptImg = document.getElementById('receipt-image');
    modalImg.src = receiptImg.src;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Close image modal
 */
function closeImageModal(event) {
    // Close only if clicking on modal background or close button
    if (event && event.target.id !== 'imageModal') return;
    
    const modal = document.getElementById('imageModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Expose functions to global scope
window.openImageModal = openImageModal;
window.closeImageModal = closeImageModal;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadReceipt();
});