import { getReceiptById, updateReceipt, deleteReceipt, updateReceiptProducts } from '../api/receipts_api.js';
import { getMerchants } from '../api/merchants_api.js';
import { getProducts } from '../api/products_api.js';

let currentReceiptId = null;
let currentReceipt = null;
let allMerchants = [];
let allProducts = [];

/**
 * Get receipt ID from URL
 */
function getReceiptIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id'));
}

/**
 * Load merchants for dropdown
 */
async function loadMerchants() {
    try {
        allMerchants = await getMerchants();
        const select = document.getElementById('receiptMerchant');
        select.innerHTML = '<option value="">Select a merchant</option>';
        
        allMerchants.forEach(merchant => {
            const option = document.createElement('option');
            option.value = merchant.id;
            option.textContent = merchant.name;
            select.appendChild(option);
        });
        
        console.log('Merchants loaded:', allMerchants.length);
        return true;
    } catch (error) {
        console.error('Erro ao carregar comerciantes:', error);
        return false;
    }
}

/**
 * Load all products for the dropdown
 */
async function loadProducts() {
    try {
        const response = await getProducts({ skip: 0, limit: 1000 });  // Use 1000 instead of 10000
        
        allProducts = Array.isArray(response) ? response : response.data || [];
        
        console.log('Products loaded:', allProducts.length);
        console.log('Sample product:', allProducts[0]);
        
        return true;
    } catch (error) {
        console.warn('Warning: Could not load products:', error.message);
        allProducts = [];
        return true;
    }
}

/**
 * Load receipt and populate form
 */
async function loadReceipt() {
    try {
        currentReceiptId = getReceiptIdFromUrl();
        if (!currentReceiptId) {
            alert('Receipt ID not provided');
            window.location.href = 'list.html';
            return;
        }

        console.log('Loading receipt ID:', currentReceiptId);

        // Load merchants FIRST
        const merchantsLoaded = await loadMerchants();
        if (!merchantsLoaded) {
            throw new Error('Failed to load merchants');
        }
        
        // Load products (don't block if it fails)
        await loadProducts();
        
        // Then load receipt
        currentReceipt = await getReceiptById(currentReceiptId);
        console.log('Receipt loaded:', currentReceipt);
        
        // Update page title
        document.querySelector('.page-title').textContent =
            `Edit Receipt: ${currentReceipt.barcode || `RCPT-${currentReceiptId}`}`;
        
        // THEN populate form
        populateForm(currentReceipt);
        
    } catch (error) {
        console.error('Erro ao carregar recibo:', error);
        alert('Erro ao carregar recibo: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate form with receipt data (VALUES, not placeholders)
 */
function populateForm(receipt) {
    console.log('Populating form with:', receipt);
    
    // Receipt code / barcode
    const codeField = document.getElementById('receiptCode');
    codeField.value = receipt.barcode || '';
    console.log('Set receiptCode to:', codeField.value);
    
    // Merchant dropdown – select actual merchant
    const merchantSelect = document.getElementById('receiptMerchant');
    merchantSelect.value = receipt.merchant_id || '';
    console.log('Set receiptMerchant to:', merchantSelect.value);
    
    // Date & time for datetime-local
    const dateField = document.getElementById('receiptDate');
    if (receipt.purchase_date) {
        const receiptDate = new Date(receipt.purchase_date);
        const localDateTime = receiptDate.toISOString().slice(0, 16); // yyyy-MM-ddTHH:mm
        dateField.value = localDateTime;
        console.log('Set receiptDate to:', dateField.value);
    } else {
        dateField.value = '';
        console.log('No purchase_date found, leaving receiptDate empty');
    }
    
    // Notes
    const notesField = document.getElementById('receiptNotes');
    notesField.value = receipt.notes || '';
    console.log('Set receiptNotes to:', notesField.value);
    
    // Render products
    renderProducts(receipt.products || []);
}

/**
 * Render products list – values filled in
 */
function renderProducts(products) {
    const container = document.getElementById('products-list');
    container.innerHTML = '';

    products.forEach((product, index) => {
        const price = parseFloat(product.price) || 0;
        const quantity = parseFloat(product.quantity) || 1;
        const productName = product.product_list?.name || product.name || 'Unknown';
        const productListId = product.product_list?.id;
        
        const item = document.createElement('div');
        item.className = 'list-item receipt-products-edit-grid';
        item.setAttribute('data-product-list-id', productListId);
        item.innerHTML = `
            <input
                type="text"
                class="form-input-compact"
                value="${productName}"
                placeholder="Product name"
                data-product-index="${index}"
                data-field="name"
                disabled
            >
            <input
                type="number"
                class="form-input-compact form-input-number-xs"
                value="${quantity}"
                min="1"
                step="0.01"
                data-product-index="${index}"
                data-field="quantity"
            >
            <input
                type="number"
                class="form-input-compact form-input-number-sm"
                value="${price.toFixed(2)}"
                step="0.01"
                min="0"
                data-product-index="${index}"
                data-field="price"
            >
            <button
                class="btn btn-sm btn-danger btn-icon-sm"
                data-action="remove-product"
                data-product-index="${index}"
            >−</button>
        `;
        container.appendChild(item);
    });

    updateProductCount();
}

/**
 * Update product count
 */
function updateProductCount() {
    const productsList = document.getElementById('products-list');
    const productsTitle = document.getElementById('products-title');
    if (productsList && productsTitle) {
        const count = productsList.querySelectorAll('.list-item').length;
        productsTitle.textContent = `Products in Receipt (${count})`;
    }
}

/**
 * Add new product with searchable dropdown selection
 */
function addProduct() {
    const productsList = document.getElementById('products-list');
    const item = document.createElement('div');
    item.className = 'list-item receipt-products-edit-grid';
    item.setAttribute('data-product-id', 'new');
    
    console.log('Adding product, total products available:', allProducts.length);
    
    // Create product select dropdown
    let productOptions = '<option value="">-- Select a product --</option>';
    allProducts.forEach(product => {
        productOptions += `<option value="${product.id}" data-name="${product.name}">${product.name}</option>`;
    });
    
    item.innerHTML = `
        <select
            class="form-input-compact product-select"
            data-field="product"
            required
        >
            ${productOptions}
        </select>
        <input
            type="number"
            class="form-input-compact form-input-number-xs"
            value="1"
            min="1"
            step="0.01"
            data-field="quantity"
        >
        <input
            type="number"
            class="form-input-compact form-input-number-sm"
            value="0.00"
            step="0.01"
            min="0"
            data-field="price"
        >
        <button
            class="btn btn-sm btn-danger btn-icon-sm"
            data-action="remove-product"
        >−</button>
    `;
    productsList.appendChild(item);
    
    // Add event listener for product selection
    const selectEl = item.querySelector('.product-select');
    selectEl.addEventListener('change', function() {
        const selectedProductId = parseInt(this.value);
        if (selectedProductId) {
            // User needs to enter price manually since ProductList doesn't have price
            const priceInput = item.querySelector('input[data-field="price"]');
            priceInput.focus(); // Focus on price field to enter it
        }
    });
    
    // Add search filtering to dropdown
    selectEl.addEventListener('keyup', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const options = selectEl.querySelectorAll('option:not(:first-child)');
        
        options.forEach(option => {
            const productName = option.textContent.toLowerCase();
            option.style.display = productName.includes(searchTerm) ? 'block' : 'none';
        });
    });
    
    updateProductCount();
}

/**
 * Remove product
 */
function removeProduct(button) {
    button.closest('.list-item').remove();
    updateProductCount();
}

/**
 * Collect products from form
 */
function getProductsFromForm() {
    const productsList = document.getElementById('products-list');
    const products = [];
    
    productsList.querySelectorAll('.list-item').forEach(item => {
        const productListId = item.getAttribute('data-product-list-id');
        const productSelect = item.querySelector('.product-select');
        const quantityInput = item.querySelector('input[data-field="quantity"]');
        const priceInput = item.querySelector('input[data-field="price"]');
        
        // Handle new products from dropdown
        if (productSelect && productSelect.value) {
            products.push({
                product_list_id: parseInt(productSelect.value),
                price: parseFloat(priceInput.value) || 0,
                quantity: parseFloat(quantityInput.value) || 1
            });
        }
        // Handle existing products
        else if (productListId && productListId !== 'new' && productListId !== 'null') {
            products.push({
                product_list_id: parseInt(productListId),
                price: parseFloat(priceInput.value) || 0,
                quantity: parseFloat(quantityInput.value) || 1
            });
        }
    });
    
    return products;
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();

    try {
        const receiptData = {
            merchant_id: parseInt(document.getElementById('receiptMerchant').value),
            purchase_date: document.getElementById('receiptDate').value.split('T')[0],
            barcode: document.getElementById('receiptCode').value || null,
            notes: document.getElementById('receiptNotes').value || null
        };

        // Update receipt metadata
        await updateReceipt(currentReceiptId, receiptData);
        
        // Get products from form
        const products = getProductsFromForm();
        console.log('Products to save:', products);
        
        // Update products
        await updateReceiptProducts(currentReceiptId, products);
        
        alert('Recibo atualizado com sucesso!');
        window.location.href = `view.html?id=${currentReceiptId}`;
    } catch (error) {
        console.error('Erro ao atualizar recibo:', error);
        alert('Erro ao atualizar recibo: ' + error.message);
    }
}

/**
 * Delete current receipt
 */
async function deleteCurrentReceipt() {
    if (!confirm('Tem a certeza que deseja eliminar este recibo?')) return;

    try {
        await deleteReceipt(currentReceiptId);
        alert('Recibo eliminado com sucesso!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Erro ao eliminar recibo:', error);
        alert('Erro ao eliminar recibo: ' + error.message);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadReceipt();

    // Form submit
    const form = document.getElementById('editReceiptForm');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }

    // Delete button
    const deleteBtn = document.querySelector('[data-action="delete-receipt"]');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            deleteCurrentReceipt();
        });
    }

    // Add product button
    const addBtn = document.querySelector('[data-action="add-product"]');
    if (addBtn) {
        addBtn.addEventListener('click', function(e) {
            e.preventDefault();
            addProduct();
        });
    }

    // Remove product buttons (delegation)
    const productsList = document.getElementById('products-list');
    if (productsList) {
        productsList.addEventListener('click', function(e) {
            const removeBtn = e.target.closest('[data-action="remove-product"]');
            if (removeBtn) {
                removeProduct(removeBtn);
            }
        });
    }
});

// Expose to global scope
window.deleteCurrentReceipt = deleteCurrentReceipt;
