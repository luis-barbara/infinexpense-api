// Receipt Edit Page - Product Management
// Handles dynamic product list in receipt edit form

// Update product count in title
function updateProductCount() {
    const productsList = document.getElementById('products-list');
    const productsTitle = document.getElementById('products-title');
    if (!productsList || !productsTitle) return;
    
    const count = productsList.querySelectorAll('.list-item').length;
    productsTitle.textContent = `Products in Receipt (${count})`;
}

// Add new product row
function addProduct() {
    const productsList = document.getElementById('products-list');
    if (!productsList) return;
    
    const newProduct = document.createElement('div');
    newProduct.className = 'list-item receipt-products-edit-grid';
    newProduct.innerHTML = `
        <input type="text" class="form-input-compact" value="" placeholder="Product name">
        <input type="number" class="form-input-compact form-input-number-xs" value="1" min="1">
        <input type="number" class="form-input-compact form-input-number-sm" value="0.00" step="0.01" min="0">
        <input type="checkbox" class="checkbox-large">
        <button class="btn btn-sm btn-danger btn-icon-sm" data-action="remove-product">−</button>
    `;
    
    productsList.appendChild(newProduct);
    updateProductCount();
    
    // Focus on the product name input
    const nameInput = newProduct.querySelector('input[type="text"]');
    if (nameInput) nameInput.focus();
}

// Remove product row
function removeProduct(button) {
    const productItem = button.closest('.list-item');
    if (productItem) {
        productItem.remove();
        updateProductCount();
    }
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add product button
    const addBtn = document.querySelector('[data-action="add-product"]');
    if (addBtn) {
        addBtn.addEventListener('click', addProduct);
    }
    
    // Remove product buttons (event delegation)
    const productsList = document.getElementById('products-list');
    if (productsList) {
        productsList.addEventListener('click', function(e) {
            const removeBtn = e.target.closest('[data-action="remove-product"]');
            if (removeBtn) {
                removeProduct(removeBtn);
            }
        });
    }
    
    // Initialize count
    updateProductCount();
});
