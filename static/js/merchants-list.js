/**
 * Merchants List - Search and Sort Functionality
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. This script works with dynamically generated merchant items
 * 2. Each merchant item must have class="merchant-item"
 * 3. Required data attributes: data-name, data-location, data-receipts, data-spent
 * 4. Container ID: merchantsList
 * 5. Search input ID: searchInput
 * 
 * USAGE:
 * - filterItems() - Called on search input change
 * - sortMerchants(field, direction) - Sort by any data attribute field
 * 
 * @example
 * // HTML Structure Required:
 * // <input id="searchInput" oninput="filterItems()">
 * // <div id="merchantsList">
 * //   <div class="merchant-item" data-name="Store" data-location="City" data-spent="687.40">...</div>
 * // </div>
 */

let sortDirection = {};

/**
 * Filter merchants based on search input
 * Searches through all text content within merchant items
 * Shows/hides items based on match
 * 
 * @function filterItems
 * @listens input#searchInput
 */
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const allItems = document.querySelectorAll('.merchant-item');

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
 * Sort merchants by specified field and direction
 * Automatically converts numeric fields (receipts, spent)
 * Keeps string fields (name, location) as text comparison
 * 
 * @function sortMerchants
 * @param {string} field - The data attribute to sort by (without 'data-' prefix)
 *                         Examples: 'name', 'location', 'receipts', 'spent'
 * @param {string} direction - Sort direction: 'asc' or 'desc'
 * 
 * @example
 * sortMerchants('spent', 'desc');  // Sort by amount spent, highest first
 * sortMerchants('name', 'asc');    // Sort alphabetically by name
 */
function sortMerchants(field, direction) {
    const container = document.getElementById('merchantsList');
    const items = Array.from(container.querySelectorAll('.merchant-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'receipts' || field === 'spent') {
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
