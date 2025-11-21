import { getProductById } from '../api/products_api.js';

let currentProductId = null;
let currentProduct = null;

/**
 * Get product ID from URL
 */
function getProductIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Load product details from API
 */
async function loadProduct() {
    try {
        currentProductId = getProductIdFromUrl();
        if (!currentProductId) {
            alert('Product ID not provided');
            window.location.href = 'list.html';
            return;
        }

        console.log('Loading product ID:', currentProductId);
        currentProduct = await getProductById(currentProductId);
        console.log('Product loaded:', currentProduct);
        
        populateProduct(currentProduct);
    } catch (error) {
        console.error('Erro ao carregar produto:', error);
        alert('Erro ao carregar produto: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate product details
 */
function populateProduct(product) {
    // Set title
    const title = document.querySelector('.page-title');
    if (title) {
        title.textContent = product.name;
    }
    
    // Set edit button link
    const editBtn = document.querySelector('a[href*="edit"]');
    if (editBtn) {
        editBtn.href = `edit.html?id=${product.id}`;
    }
    
    // Set delete button
    const deleteBtn = document.querySelector('button.btn-danger');
    if (deleteBtn) {
        deleteBtn.onclick = function() {
            deleteProduct();
        };
    }
    
    // Product Info
    const categoryEl = document.querySelector('[data-field="category"]');
    if (categoryEl) {
        categoryEl.textContent = product.category?.name || '-';
    }
    
    const volumeEl = document.querySelector('[data-field="volume"]');
    if (volumeEl) {
        volumeEl.textContent = product.measurement_unit?.name || '-';
    }
    
    const barcodeEl = document.querySelector('[data-field="barcode"]');
    if (barcodeEl) {
        barcodeEl.textContent = product.barcode || '-';
    }
    
    // Product photo
    if (product.product_list_photo) {
        const img = document.getElementById('product-image');
        img.src = product.product_list_photo;
        img.style.display = 'block';
        document.getElementById('no-photo-placeholder').style.display = 'none';
    }
}

/**
 * Delete product with confirmation
 */
async function deleteProduct() {
    if (!confirm('Tem a certeza que deseja eliminar este produto?')) return;

    try {
        const { deleteProduct: deleteProductAPI } = await import('../api/products_api.js');
        await deleteProductAPI(currentProductId);
        alert('Produto eliminado com sucesso!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Erro ao eliminar produto:', error);
        alert('Não é possível eliminar este produto:\n\n' + error.message);
    }
}

// Expose to global scope
window.deleteProduct = deleteProduct;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProduct();
});