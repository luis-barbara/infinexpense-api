import { getProducts } from '/static/api/products_api.js';

let allProducts = [];
let sortDirection = {};

/**
 * Load products from API
 */
async function loadProducts() {
    try {
        const products = await getProducts({ skip: 0, limit: 1000 });
        allProducts = Array.isArray(products) ? products : products.data || [];
        
        console.log('Products loaded:', allProducts.length);
        renderProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

/**
 * Render products to the DOM
 */
function renderProducts(products) {
    const container = document.getElementById('productsList');
    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center;">No products found.</div>';
        return;
    }

    products.forEach(product => {
        const item = document.createElement('div');
        item.className = 'list-item product-item';
        item.setAttribute('data-name', product.name);
        item.setAttribute('data-category', product.category?.name || 'N/A');
        item.setAttribute('data-volume', product.measurement_unit?.name || 'N/A');
        item.setAttribute('data-barcode', product.barcode || 'N/A');
        item.setAttribute('data-price', '0.00');
        item.style.display = 'grid';
        item.style.gridTemplateColumns = '1fr 1fr 0.8fr 1fr 0.6fr';
        item.style.gap = '1rem';
        item.style.padding = '1rem';
        item.style.borderBottom = '1px solid hsl(var(--border) / 0.2)';
        item.style.alignItems = 'center';

        item.innerHTML = `
            <div><span>${product.name}</span></div>
            <div><span>${product.category?.name || 'N/A'}</span></div>
            <div><span>${product.measurement_unit.name} - ${product.measurement_unit?.abbreviation || 'N/A'}</span></div>
            <div><span>${product.barcode || 'N/A'}</span></div>
            <div style="display: flex; gap: 0.5rem; justify-content: flex-start;">
                <a href="/static/product/view.html?id=${product.id}" class="btn btn-secondary btn-sm" title="View">👁️</a>
                <a href="/static/product/edit.html?id=${product.id}" class="btn btn-secondary btn-sm" title="Edit">✏️</a>
                <button class="btn btn-danger btn-sm" title="Delete" onclick="confirmDelete(${product.id})">🗑️</button>
            </div>
        `;

        container.appendChild(item);
    });
}

/**
 * Filter products based on search input
 */
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const allItems = document.querySelectorAll('.product-item');

    allItems.forEach(item => {
        const productName = item.getAttribute('data-name').toLowerCase();
        const category = item.getAttribute('data-category').toLowerCase();
        const barcode = item.getAttribute('data-barcode').toLowerCase();
        
        // Check if search term matches any of the fields
        const matches = 
            productName.includes(searchTerm) ||
            category.includes(searchTerm) ||
            barcode.includes(searchTerm);
        
        item.style.display = (matches || searchTerm === '') ? 'grid' : 'none';
    });
}

/**
 * Sort products by specified field and direction
 */
function sortProducts(field, direction) {
    const container = document.getElementById('productsList');
    const items = Array.from(container.querySelectorAll('.product-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'price') {
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
 * Delete product with confirmation
 */
async function confirmDelete(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;

    try {
        const { deleteProduct } = await import('/static/api/products_api.js');
        await deleteProduct(productId);
        alert('Product deleted successfully!');
        loadProducts(); // Reload list
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('Error deleting product: ' + error.message);
    }
}

// Expose to global scope
window.filterItems = filterItems;
window.sortProducts = sortProducts;
window.confirmDelete = confirmDelete;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    
    // Add real-time filtering
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', filterItems);
    }
});
