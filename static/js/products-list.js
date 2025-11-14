/**
 * Products List - Search and Sort Functionality
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. This script works with dynamically generated product items
 * 2. Each product item must have class="product-item"
 * 3. Required data attributes: data-name, data-category, data-barcode, data-volume, data-price
 * 4. Container ID: productsList
 * 5. Search input ID: searchInput
 * 
 * USAGE:
 * - filterItems() - Called on search input change
 * - sortProducts(field, direction) - Sort by any data attribute field
 * 
 * @example
 * // HTML Structure Required:
 * // <input id="searchInput" oninput="filterItems()">
 * // <div id="productsList">
 * //   <div class="product-item" data-name="Milk" data-category="Dairy" data-price="0.89">...</div>
 * // </div>
 */

let sortDirection = {};

/**
 * Filter products based on search input
 * Searches through all text content within product items
 * Shows/hides items based on match
 * 
 * @function filterItems
 * @listens input#searchInput
 */
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const allItems = document.querySelectorAll('.product-item');

    allItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        const matches = text.includes(searchTerm);
        
        if (matches || searchTerm === '') {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

/**
 * Sort products by specified field and direction
 * Automatically converts numeric fields (price, quantity)
 * Keeps string fields (name, category, barcode) as text comparison
 * 
 * @function sortProducts
 * @param {string} field - The data attribute to sort by (without 'data-' prefix)
 *                         Examples: 'name', 'category', 'price', 'barcode'
 * @param {string} direction - Sort direction: 'asc' or 'desc'
 * 
 * @example
 * sortProducts('price', 'asc');    // Sort by price, lowest first
 * sortProducts('name', 'asc');     // Sort alphabetically by name
 */
function sortProducts(field, direction) {
    const container = document.getElementById('productsList');
    const items = Array.from(container.querySelectorAll('.product-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'price' || field === 'quantity') {
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
