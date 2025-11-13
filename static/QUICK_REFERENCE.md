# InfinExpense - Quick Reference Guide

A cheat sheet for developers working on the InfinExpense frontend.

## 📂 Project Files

```
src_temp/
├── index.html                    # Dashboard (stats + recent receipts)
├── receipts.html                 # All receipts (paginated list)
├── receipt-1001.html            # Receipt detail (editable)
├── receipt-add.html             # Add new receipt form
├── products.html                 # All products (paginated list)
├── product-2001.html            # Product detail + price chart
├── product-add.html             # Add new product form
├── product-edit-2001.html       # Edit product form
├── categories.html              # Categories + pie chart
├── category-add.html            # Add new category form
├── category-edit-3001.html      # Edit category form
├── merchants.html               # All merchants (paginated list)
├── merchant-add.html            # Add new merchant form
├── merchant-edit-4001.html      # Edit merchant form
├── styles.css                   # Main stylesheet (organized)
├── styles_old.css               # Backup (original)
├── README.md                    # Main documentation
├── BACKEND_INTEGRATION.md       # Backend/DB guide
└── CSS_ORGANIZATION.md          # CSS structure guide
```

## 🎨 CSS Quick Reference

### CSS Variables (colors)
```css
var(--primary-color)    /* #2563eb - Blue */
var(--success-color)    /* #10b981 - Green */
var(--danger-color)     /* #ef4444 - Red */
var(--warning-color)    /* #f59e0b - Orange */
var(--secondary-color)  /* #64748b - Gray */
```

### Common Classes
```css
.btn                    /* Button base */
.btn-primary           /* Blue button */
.btn-danger            /* Red button (delete) */
.btn-outline           /* Transparent with border */

.card                  /* White card container */
.stat-card             /* Statistics display */
.receipt-card          /* Receipt display */

.form-input            /* Text input */
.form-select           /* Dropdown */
.form-textarea         /* Multi-line input */

.list-item             /* List row */
.pagination            /* Pagination wrapper */

.text-center           /* Center text */
.mb-2                  /* Margin bottom 1rem */
.flex-between          /* Space between items */
```

### CSS Sections
1. Reset & Base Styles (variables, resets)
2. Layout Components (navbar, container, grids)
3. Card Components (stat-card, receipt-card)
4. Button Components (all button variants)
5. Form Components (inputs, selects, textareas)
6. List & Table Components (list-item, tables)
7. Pagination & Navigation (pagination controls)
8. Detail Page Components (detail views)
9. Chart & Visualization (Chart.js containers)
10. Badges & Status Indicators (status badges)
11. Utility Classes (spacing, flex, text)
12. Responsive Design (@media queries)

## 🔌 Data Attributes

### Receipts
```html
data-receipt-id="1001"          <!-- Receipt ID (PK) -->
data-merchant-id="4001"         <!-- Merchant ID (FK) -->
data-field="merchant-name"      <!-- Field identifier -->
data-field="receipt-date"       <!-- Date field -->
data-field="receipt-total"      <!-- Total amount -->
data-field="product-count"      <!-- Item count -->
```

### Products
```html
data-product-id="2001"          <!-- Product ID (PK) -->
data-category-id="3001"         <!-- Category ID (FK) -->
data-field="product-name"       <!-- Product name -->
data-field="product-price"      <!-- Current price -->
```

### Categories
```html
data-category-id="3001"         <!-- Category ID (PK) -->
data-color="#4169E1"            <!-- Chart color -->
data-field="category-name"      <!-- Category name -->
data-field="spending-total"     <!-- Total spending -->
```

### Merchants
```html
data-merchant-id="4001"         <!-- Merchant ID (PK) -->
data-field="merchant-name"      <!-- Merchant name -->
data-field="receipt-count"      <!-- Receipt count -->
```

## 📜 JavaScript Functions

### Pagination (receipts.html, products.html, merchants.html)
```javascript
showPage(page)             // Display specific page (1-indexed)
updatePagination()         // Refresh pagination controls
changePage(direction)      // Navigate (-1=prev, +1=next)
changeItemsPerPage()       // Change items per page (5/10/20/50)
filterItems()              // Search/filter items
```

### Dashboard (index.html)
```javascript
toggleComparisonMode()     // Toggle "+12.5%" ↔ "+€314.52"
```

### Receipt Editing (receipt-1001.html)
```javascript
updateProduct(input)       // Update amount/price, recalc total
removeProduct(button)      // Delete product from receipt
calculateTotal()           // Recalculate receipt total
```

### Variables
```javascript
itemsPerPage               // Current items per page (default: 5)
currentPage                // Current page number
allItems                   // NodeList of all items
totalItems                 // Total item count
```

## 🗃️ Database Schema

### Tables
```sql
merchants (id, name, location)
categories (id, name, color, icon)
receipts (id, merchant_id, date, total, image_path)
products (id, name, category_id, description)
receipt_items (id, receipt_id, product_id, amount, price)
```

### Key Relationships
- `receipts.merchant_id` → `merchants.id`
- `products.category_id` → `categories.id`
- `receipt_items.receipt_id` → `receipts.id`
- `receipt_items.product_id` → `products.id`

## 🔗 API Endpoints (Backend Integration)

### GET Routes
```
/                               # Dashboard
/receipts                       # Receipts list
/receipt/<id>                   # Receipt detail
/products                       # Products list
/product/<id>                   # Product detail
/categories                     # Categories list
/merchants                      # Merchants list
```

### API Endpoints
```
GET  /api/categories/spending               # Category spending data
GET  /api/products/<id>/price-history       # Price history data
POST /api/receipts                          # Create receipt
POST /api/products                          # Create product
PATCH /api/receipt-items/<id>               # Update receipt item
DELETE /api/receipt-items/<id>              # Delete receipt item
```

## 📊 Chart.js Integration

### Category Pie Chart (categories.html)
```javascript
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Dairy', 'Bakery', ...],
        datasets: [{
            data: [450.50, 320.75, ...],
            backgroundColor: ['#4169E1', '#32CD32', ...]
        }]
    }
});
```

### Price History Line Chart (product-2001.html)
```javascript
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['2025-11-01', '2025-11-05', ...],
        datasets: [{
            data: [0.89, 0.85, 0.92, ...],
            borderColor: '#2563eb'
        }]
    }
});
```

## 🎯 Common Tasks

### Add New Receipt List Item
```html
<a href="receipt-1011.html" 
   class="list-item receipt-item" 
   data-receipt-id="1011" 
   data-merchant-id="4001">
    <div class="list-item-main">
        <div>
            <div class="list-item-label">Receipt ID</div>
            <div class="list-item-value" data-field="receipt-id">#1011</div>
        </div>
        <div>
            <div class="list-item-label">Merchant</div>
            <div class="list-item-value" data-field="merchant-name">Continente</div>
        </div>
        <div>
            <div class="list-item-label">Date</div>
            <div class="list-item-value" data-field="receipt-date">Nov 12, 2025</div>
        </div>
        <div>
            <div class="list-item-label">Total</div>
            <div class="list-item-value" data-field="receipt-total">€75.30</div>
        </div>
    </div>
</a>
```

### Add New Button
```html
<button class="btn btn-primary" onclick="myFunction()">
    Add Item
</button>

<button class="btn btn-danger" onclick="deleteItem()">
    Delete
</button>

<button class="btn btn-outline btn-sm">
    Cancel
</button>
```

### Add New Form Input
```html
<div class="form-group">
    <label for="productName" class="form-label">Product Name</label>
    <input type="text" 
           id="productName" 
           name="name"
           class="form-input" 
           data-field="product-name"
           placeholder="Enter product name"
           required>
</div>
```

### Add New Stat Card
```html
<div class="stat-card" data-stat-type="custom-stat">
    <div class="stat-label">Total Products</div>
    <div class="stat-value" id="total-products" data-field="product-count">
        257
    </div>
    <div class="card-subtitle">
        +12 from last month
    </div>
</div>
```

## 🔍 Debugging Tips

### Check Data Attributes
```javascript
// Get receipt ID from clicked element
const receiptId = element.getAttribute('data-receipt-id');

// Get all receipts
const receipts = document.querySelectorAll('[data-receipt-id]');

// Filter by merchant
const continenteReceipts = document.querySelectorAll('[data-merchant-id="4001"]');
```

### Console Debugging
```javascript
// Check pagination state
console.log('Current page:', currentPage);
console.log('Items per page:', itemsPerPage);
console.log('Total items:', totalItems);

// Check item visibility
allItems.forEach(item => {
    console.log('Visible:', item.getAttribute('data-visible'));
});
```

### CSS Debugging
```css
/* Add temporary borders to see layout */
.receipt-card { border: 2px solid red !important; }
.list-item { border: 2px solid blue !important; }

/* Check z-index issues */
.navbar { background: rgba(255,0,0,0.3) !important; }
```

## 📱 Responsive Breakpoints

- **Desktop**: Default styles (> 768px)
- **Mobile**: `@media (max-width: 768px)`

### Mobile Changes
- Grids: 3 columns → 1 column
- Navigation: Simplified
- Cards: Full width
- Tables: Horizontal scroll
- Buttons: Full width on forms

## ⚡ Performance Tips

1. **Minimize HTTP Requests**
   - Chart.js loaded via CDN
   - Inline JavaScript (no extra files)

2. **Optimize Images**
   - Receipt images: < 500KB
   - Compress before upload

3. **Efficient Pagination**
   - Show only 5-10 items by default
   - Use backend pagination for large datasets

4. **CSS Loading**
   - Single stylesheet
   - Minify for production

## 🔐 Security Notes

- **Input Validation**: Always validate server-side
- **SQL Injection**: Use parameterized queries
- **XSS Prevention**: Escape HTML output
- **File Uploads**: Validate file types and sizes
- **CSRF**: Add CSRF tokens to forms in production

## 📦 Dependencies

- **Chart.js**: v3+ (CDN loaded)
- **No jQuery**: Vanilla JavaScript only
- **No Bootstrap**: Custom CSS

## 🚀 Production Checklist

- [ ] Minify `styles.css` → `styles.min.css`
- [ ] Add CSRF tokens to all forms
- [ ] Implement server-side validation
- [ ] Add error handling to JavaScript
- [ ] Test on Chrome, Firefox, Safari
- [ ] Test mobile responsiveness
- [ ] Optimize images
- [ ] Add loading states
- [ ] Implement authentication
- [ ] Set up proper database indexes

## 📞 Support

For detailed information, see:
- **README.md** - Project overview and structure
- **BACKEND_INTEGRATION.md** - Python/DB integration guide
- **CSS_ORGANIZATION.md** - Complete CSS documentation

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**License**: Educational (ETIC Algarve)
