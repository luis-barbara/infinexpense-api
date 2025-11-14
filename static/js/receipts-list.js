/**
 * Receipts List - Search and Sort Functionality
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. This script works with dynamically generated receipt items
 * 2. Each receipt item must have class="receipt-item" 
 * 3. Required data attributes: data-receipt-id, data-merchant, data-date, data-products, data-total
 * 4. Container ID: receiptsList
 * 5. Search input ID: searchInput
 * 
 * USAGE:
 * - filterItems() - Called on search input change
 * - sortReceipts(field, direction) - Sort by any data attribute field
 * 
 * @example
 * // HTML Structure Required:
 * // <input id="searchInput" oninput="filterItems()">
 * // <div id="receiptsList">
 * //   <div class="receipt-item" data-merchant="Store" data-date="2025-11-10" data-total="87.45">...</div>
 * // </div>
 */

let sortDirection = {};

/**
 * Filter receipts based on search input
 * Searches through all text content within receipt items
 * Shows/hides items based on match
 * 
 * @function filterItems
 * @listens input#searchInput
 */
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const allItems = document.querySelectorAll('.receipt-item');

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
 * Sort receipts by specified field and direction
 * Automatically converts numeric fields (receipt-id, products, total)
 * Keeps string fields (merchant, date) as text comparison
 * 
 * @function sortReceipts
 * @param {string} field - The data attribute to sort by (without 'data-' prefix)
 *                         Examples: 'receipt-id', 'merchant', 'date', 'products', 'total'
 * @param {string} direction - Sort direction: 'asc' or 'desc'
 * 
 * @example
 * sortReceipts('total', 'desc'); // Sort by total amount, highest first
 * sortReceipts('date', 'asc');   // Sort by date, oldest first
 */
function sortReceipts(field, direction) {
    const container = document.getElementById('receiptsList');
    const items = Array.from(container.querySelectorAll('.receipt-item'));
    
    items.sort((a, b) => {
        let aValue = a.getAttribute('data-' + field);
        let bValue = b.getAttribute('data-' + field);
        
        // Convert to numbers for numeric fields
        if (field === 'receipt-id' || field === 'products' || field === 'total') {
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
