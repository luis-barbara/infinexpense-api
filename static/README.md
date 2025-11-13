# InfinExpense - Receipt Management System Frontend

A modern, responsive web interface for managing receipts, products, merchants, and categories with fictional data for demonstration purposes.

## 📁 Project Structure

```
infinexpense-frontend/
├── styles.css                  # Main stylesheet (organized by component type)
├── index.html                  # Dashboard with monthly statistics
├── receipts.html              # List of all receipts with pagination
├── receipt-1001.html          # Individual receipt detail page
├── receipt-add.html           # Form to add new receipt
├── products.html              # List of all products with pagination
├── product-2001.html          # Individual product detail page
├── product-add.html           # Form to add new product
├── product-edit-2001.html     # Form to edit existing product
├── categories.html            # Categories with pie chart visualization
├── category-add.html          # Form to add new category
├── category-edit-3001.html    # Form to edit existing category
├── merchants.html             # List of all merchants with pagination
├── merchant-add.html          # Form to add new merchant
├── merchant-edit-4001.html    # Form to edit existing merchant
└── README.md                  # This file
```

## 🎨 CSS Architecture

The `styles.css` file is organized into 12 clear sections:

### 1. Reset & Base Styles
- Box model reset
- CSS variables (color palette, shadows, spacing)
- Base body styles

### 2. Layout Components
- Navigation bar (`.navbar`, `.nav-container`, `.nav-menu`, `.nav-link`)
- Main container (`.container`)
- Page headers (`.page-header`, `.page-title`)
- Grid layouts (`.grid`, `.grid-2`, `.grid-3`, `.stats-grid`)

### 3. Card Components
- Base card (`.card`)
- Statistics card (`.stat-card`, `.stat-label`, `.stat-value`)
- Receipt card (`.receipt-card`, `.receipt-header`, `.receipt-merchant`)

### 4. Button Components
- Base button (`.btn`)
- Variants: `.btn-primary`, `.btn-secondary`, `.btn-success`, `.btn-danger`, `.btn-outline`
- Sizes: `.btn-sm`

### 5. Form Components
- Form groups (`.form-group`, `.form-label`)
- Inputs (`.form-input`, `.form-select`, `.form-textarea`)
- Search bar (`.search-bar`, `.search-input`)
- File upload (`.file-upload`)

### 6. List & Table Components
- List container (`.list-container`, `.list-item`)
- Scrollable lists (`.scrollable-list`)
- Tables (`.table-container`, `.table`)

### 7. Pagination & Navigation
- Pagination controls (`.pagination`, `.pagination-btn`)

### 8. Detail Page Components
- Detail headers (`.detail-header`, `.detail-title`, `.detail-info`)

### 9. Chart & Visualization Components
- Chart containers (`.chart-container`)
- Image previews (`.image-preview`)

### 10. Badges & Status Indicators
- Badges (`.badge`, `.badge-primary`, `.badge-success`, `.badge-warning`)

### 11. Utility Classes
- Text alignment, spacing, flexbox, colors, font weights

### 12. Responsive Design
- Mobile-first breakpoints (@media queries)

## 🎯 JavaScript Functionality

### Pagination System
**Used in**: `receipts.html`, `products.html`, `merchants.html`

```javascript
/**
 * Display items for a specific page
 * @param {number} page - The page number to display (1-indexed)
 */
function showPage(page) { ... }

/**
 * Update pagination button states and page numbers
 */
function updatePagination() { ... }

/**
 * Navigate to previous/next page
 * @param {number} direction - Direction to move (-1 for previous, +1 for next)
 */
function changePage(direction) { ... }

/**
 * Change number of items displayed per page
 * Triggered by dropdown selection
 */
function changeItemsPerPage() { ... }

/**
 * Filter items based on search input
 * Shows/hides items matching search term
 */
function filterItems() { ... }
```

### Dashboard Toggle
**Used in**: `index.html`

```javascript
/**
 * Toggle between percentage and real value display for expense comparison
 * Switches between "+12.5%" and "+€314.52"
 */
function toggleComparisonMode() { ... }
```

### Receipt Editing
**Used in**: `receipt-1001.html`

```javascript
/**
 * Update product amount or price and recalculate total
 * @param {HTMLInputElement} input - The input element that changed
 */
function updateProduct(input) { ... }

/**
 * Remove a product from the receipt
 * @param {HTMLButtonElement} button - The remove button clicked
 */
function removeProduct(button) { ... }

/**
 * Recalculate receipt total based on all products
 * Updates the total display and product count
 */
function calculateTotal() { ... }
```

### Chart.js Integration
**Used in**: `categories.html`, `product-2001.html`

```javascript
// Pie Chart for Category Spending
const categoryChart = new Chart(ctx, {
    type: 'pie',
    data: { /* category data */ },
    options: { /* responsive config, tooltips */ }
});

// Line Chart for Price History
const priceChart = new Chart(ctx, {
    type: 'line',
    data: { /* price history data */ },
    options: { /* responsive config, tooltips */ }
});
```

## 🔌 Backend Integration Guide

### Data Attribute Convention

All dynamic content elements have `data-id` attributes for easy backend integration:

```html
<!-- Receipts -->
<div class="receipt-card" data-id="1001" data-merchant-id="4001">
    <!-- Receipt content -->
</div>

<!-- Products -->
<div class="list-item product-item" data-id="2001" data-category-id="3001">
    <!-- Product details -->
</div>

<!-- Categories -->
<div class="list-item category-item" data-id="3001">
    <!-- Category details -->
</div>

<!-- Merchants -->
<div class="list-item merchant-item" data-id="4001">
    <!-- Merchant details -->
</div>
```

### Element ID Naming Convention

Elements that should receive dynamic data have descriptive IDs:

```html
<!-- Dashboard Statistics -->
<span id="total-receipts">142</span>
<span id="monthly-expenses">€2,508.45</span>
<span id="expense-comparison">+12.5%</span>
<span id="products-tracked">257</span>

<!-- Receipt Details -->
<span id="receipt-id">1001</span>
<span id="receipt-merchant">Pingo Doce</span>
<span id="receipt-date">2025-11-15</span>
<span id="receipt-total">€45.67</span>

<!-- Product Details -->
<span id="product-id">2001</span>
<span id="product-name">Leite Mimosa</span>
<span id="product-category">Dairy</span>
<span id="product-price">€0.89</span>
```

### Python Integration Example

```python
from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route('/api/receipts')
def get_receipts():
    # Fetch from database
    receipts = db.execute("SELECT * FROM receipts")
    return json.dumps(receipts)

@app.route('/dashboard')
def dashboard():
    with open('index.html', 'r') as f:
        template = f.read()
    
    stats = {
        'total_receipts': db.count('receipts'),
        'monthly_expenses': db.sum('receipts.total', month='current'),
        'expense_comparison': calculate_comparison(),
        'products_tracked': db.count('products')
    }
    
    # Replace placeholder IDs with actual data
    html = template
    html = html.replace('id="total-receipts">142', f'id="total-receipts">{stats["total_receipts"]}')
    html = html.replace('id="monthly-expenses">€2,508.45', f'id="monthly-expenses">€{stats["monthly_expenses"]:.2f}')
    # ... and so on
    
    return html
```

### JavaScript Data Binding Example

```javascript
// Fetch data from Python backend
fetch('/api/receipts')
    .then(response => response.json())
    .then(receipts => {
        const container = document.querySelector('.receipt-list');
        container.innerHTML = ''; // Clear existing
        
        receipts.forEach(receipt => {
            const card = document.createElement('div');
            card.className = 'receipt-card';
            card.setAttribute('data-id', receipt.id);
            card.setAttribute('data-merchant-id', receipt.merchant_id);
            card.innerHTML = `
                <div class="receipt-header">
                    <span class="receipt-merchant">${receipt.merchant}</span>
                    <span class="receipt-date">${receipt.date}</span>
                </div>
                <div class="receipt-details">
                    <div class="receipt-detail-item">
                        <span class="receipt-detail-label">Total</span>
                        <span class="receipt-detail-value">€${receipt.total}</span>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    });
```

## 📊 Chart.js Data Binding

### Category Pie Chart

```javascript
// Fetch category data from backend
fetch('/api/categories/spending')
    .then(response => response.json())
    .then(data => {
        new Chart(document.getElementById('categoryChart'), {
            type: 'pie',
            data: {
                labels: data.map(c => c.name),
                datasets: [{
                    data: data.map(c => c.spending),
                    backgroundColor: data.map(c => c.color)
                }]
            }
        });
    });
```

### Price History Line Chart

```javascript
// Fetch price history from backend
fetch(`/api/products/${productId}/price-history`)
    .then(response => response.json())
    .then(data => {
        new Chart(document.getElementById('priceChart'), {
            type: 'line',
            data: {
                labels: data.map(p => p.date),
                datasets: [{
                    label: 'Price',
                    data: data.map(p => p.price),
                    borderColor: '#2563eb'
                }]
            }
        });
    });
```

## 🎨 Color Palette

```css
--primary-color: #2563eb;     /* Blue - Primary actions */
--success-color: #10b981;     /* Green - Success states */
--danger-color: #ef4444;      /* Red - Danger/Delete actions */
--warning-color: #f59e0b;     /* Orange - Warnings */
--secondary-color: #64748b;   /* Gray - Secondary actions */
```

## 📱 Responsive Breakpoints

- **Desktop**: > 768px (default)
- **Mobile**: ≤ 768px (stacked layouts, full-width components)

## 🔧 Development Notes

### Adding New Pages

1. Copy an existing page as template
2. Update page `<title>` and `.page-title`
3. Update active state in navigation: add `.active` to corresponding `.nav-link`
4. Add `data-id` attributes to all dynamic elements
5. Implement JavaScript functions if needed (pagination, filtering, etc.)

### Adding New Components

1. Add CSS in appropriate section of `styles.css`
2. Follow BEM naming convention where possible
3. Use CSS variables for colors and spacing
4. Test responsiveness on mobile devices

### Performance Optimization

- Chart.js is loaded via CDN (only on pages that need it)
- Inline JavaScript minimizes HTTP requests
- CSS uses hardware-accelerated transforms for animations
- Images should be optimized before use

## 📦 Dependencies

- **Chart.js v3+**: For pie charts and line charts
  - CDN: `https://cdn.jsdelivr.net/npm/chart.js`
  - Used in: `categories.html`, `product-2001.html`

## 🚀 Getting Started

1. **Open any HTML file** in a modern web browser
2. **Navigate** using the top navigation bar
3. **Interact** with forms, buttons, and charts
4. **Test pagination** on list pages (receipts, products, merchants)
5. **Edit products** on receipt detail pages

## 🔐 Security Notes

- All forms use `POST` method (ready for backend integration)
- Input validation should be implemented server-side
- CSRF tokens should be added to forms in production
- Sanitize all user inputs before displaying

## 📝 Future Enhancements

- [ ] Add real-time search (debounced)
- [ ] Implement sorting on table columns
- [ ] Add date range pickers for filtering
- [ ] Export functionality (CSV, PDF)
- [ ] Batch operations (select multiple items)
- [ ] Dark mode toggle
- [ ] Print-friendly receipt views
- [ ] Barcode scanning integration

## 🤝 Contributing

When contributing:
1. Follow the existing code style
2. Add comments to complex logic
3. Test on Chrome, Firefox, and Safari
4. Ensure mobile responsiveness
5. Update this README if adding new features

## 📄 License

This project is part of the ETIC Algarve Database course (2025).

---

**Last Updated**: November 11, 2025  
**Version**: 1.0.0  
**Author**: [Your Name]  
**Course**: Base de Dados - ETIC Algarve
