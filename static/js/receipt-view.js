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
    
    // Products
    renderProducts(receipt.products || []);
    
    // Image
    if (receipt.receipt_photo) {
        const img = document.getElementById('receipt-image');
        img.src = receipt.receipt_photo;
        img.style.display = 'block';
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
    products.forEach((product, index) => {
        const item = document.createElement('div');
        item.className = `list-item list-row ${index % 2 === 0 ? 'row-even' : 'row-odd'}`;
        
        const price = parseFloat(product.price) || 0;
        const quantity = parseFloat(product.quantity) || 0;
        
        item.innerHTML = `
            <div class="list-item-value">${product.product_list?.name || '-'}</div>
            <div class="list-item-value">${product.product_list?.category?.name || '-'}</div>
            <div class="list-item-value">${product.product_list?.barcode || '-'}</div>
            <div class="list-item-value">${quantity.toFixed(2)}</div>
            <div class="list-item-value">${price.toFixed(2)} €</div>
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadReceipt();
});