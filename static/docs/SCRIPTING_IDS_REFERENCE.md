# InfinExpense - Scripting IDs & Data Attributes Reference

**Last Updated:** November 14, 2025  
**Purpose:** Complete reference for all HTML IDs and data attributes ready for backend scripting integration

---

## 📋 Table of Contents

1. [Dashboard (index.html)](#-dashboard-indexhtml)
2. [Receipts (receipts.html)](#-receipts-receiptshtml)
3. [Products (products.html)](#-products-productshtml)
4. [Categories (categories.html)](#-categories-categorieshtml)
5. [Merchants (merchants.html)](#-merchants-merchantshtml)
6. [Receipt Detail (receipt-1001.html)](#-receipt-detail-receipt-1001html)
7. [Product Detail (product-2001.html)](#-product-detail-product-2001html)
8. [Merchant Detail (merchant-4001.html)](#-merchant-detail-merchant-4001html)
9. [Add/Edit Forms](#-addedit-forms)
10. [Chart Elements](#-chart-elements)
11. [Search & Filter Elements](#-search--filter-elements)
12. [Quick Reference Tables](#-quick-reference-tables)

---

## 🏠 Dashboard (index.html)

### Statistics Cards

#### Monthly Expenses Card
```html
<div class="stat-card" data-stat-type="monthly-expenses">
    <div id="monthly-expenses" data-field="total-expenses">2,847.65 €</div>
    <span id="expenseComparison" data-field="expense-comparison">+12.5% from last month</span>
</div>
```
**Script Targets:**
- **ID**: `monthly-expenses` - Update with current month total
- **ID**: `expenseComparison` - Update comparison text (supports click toggle)
- **Data Field**: `total-expenses` - Main expense value
- **Data Field**: `expense-comparison` - Comparison value

#### Total Receipts Card
```html
<div class="stat-card" data-stat-type="total-receipts">
    <div id="total-receipts" data-field="receipt-count">28</div>
    <div id="receipts-comparison" data-field="receipt-comparison">+5 from last month</div>
</div>
```
**Script Targets:**
- **ID**: `total-receipts` - Update receipt count
- **ID**: `receipts-comparison` - Update comparison text
- **Data Field**: `receipt-count` - Number of receipts
- **Data Field**: `receipt-comparison` - Comparison text

#### Products Purchased Card
```html
<div class="stat-card" data-stat-type="total-products">
    <div id="products-purchased" data-field="product-count">156</div>
    <div id="products-comparison" data-field="product-comparison">+18 from last month</div>
</div>
```
**Script Targets:**
- **ID**: `products-purchased` - Update product count
- **ID**: `products-comparison` - Update comparison text
- **Data Field**: `product-count` - Number of products
- **Data Field**: `product-comparison` - Comparison text

### Recent Receipts List

```html
<div id="recent-receipts-list" data-max-items="3">
    <!-- Receipt cards go here -->
</div>
```

**Container ID**: `recent-receipts-list`  
**Attribute**: `data-max-items="3"` - Maximum number of receipts to display

#### Individual Receipt Card Structure
```html
<a href="receipt-1001.html" 
   class="receipt-card" 
   data-receipt-id="1001" 
   data-merchant-id="4001">
    
    <div class="receipt-merchant" data-field="merchant-name">Continente</div>
    <span data-field="product-count">12 items</span>
    <div class="receipt-date" data-field="receipt-date">Nov 10, 2025</div>
    <div data-field="receipt-total">87.45 €</div>
</a>
```

**Data Attributes:**
- `data-receipt-id` - Receipt unique ID
- `data-merchant-id` - Associated merchant ID
- `data-field="merchant-name"` - Merchant name
- `data-field="product-count"` - Number of products
- `data-field="receipt-date"` - Receipt date
- `data-field="receipt-total"` - Total amount

---

## 🧾 Receipts (receipts.html)

### Search Input
```html
<input type="text" 
       id="searchInput" 
       class="search-input" 
       placeholder="Search receipts...">
```
**ID**: `searchInput` - Bind search functionality

### Receipts List Container
```html
<div class="list-container" id="receiptsList">
    <!-- Receipt items go here -->
</div>
```
**Container ID**: `receiptsList` - Main list for all receipt items

### Individual Receipt Item Structure
```html
<div class="list-item receipt-item" 
     data-receipt-id="1001" 
     data-merchant="Continente" 
     data-date="2025-11-10" 
     data-products="12" 
     data-total="87.45">
    
    <div class="list-item-main receipts-list-grid">
        <div class="list-item-value">RCPT-2025-1001-CON</div>
        <div class="list-item-value">Continente</div>
        <div class="list-item-value">10/11/2025</div>
        <div class="list-item-value">12 items</div>
        <div class="list-item-value">87.45 €</div>
        <div class="list-item-actions">
            <!-- Action buttons -->
        </div>
    </div>
</div>
```

**Data Attributes:**
- `data-receipt-id` - Unique receipt ID (e.g., "1001")
- `data-merchant` - Merchant name (for filtering/sorting)
- `data-date` - Receipt date in YYYY-MM-DD format
- `data-products` - Number of products (numeric)
- `data-total` - Total amount (numeric, no currency symbol)

**Grid Columns Order:**
1. Receipt Code
2. Merchant Name
3. Date
4. Product Count
5. Total Amount
6. Actions (View/Edit/Delete)

---

## 🛒 Products (products.html)

### Search Input
```html
<input type="text" 
       id="searchInput" 
       class="search-input" 
       placeholder="Search products...">
```
**ID**: `searchInput` - Bind search functionality

### Products List Container
```html
<div class="list-container" id="productsList">
    <!-- Product items go here -->
</div>
```
**Container ID**: `productsList` - Main list for all product items

### Individual Product Item Structure
```html
<div class="list-item product-item" 
     data-name="Milk Semi-Skimmed" 
     data-category="Dairy" 
     data-volume="L" 
     data-barcode="5600308532147" 
     data-price="0.89">
    
    <div class="list-item-main products-list-grid">
        <div class="list-item-value">
            <a href="product-2001.html">Milk Semi-Skimmed</a>
        </div>
        <div class="list-item-value">Dairy</div>
        <div class="list-item-value">5600308532147</div>
        <div class="list-item-value">L</div>
        <div class="list-item-value">0.89 €</div>
        <div class="list-item-actions">
            <!-- Action buttons -->
        </div>
    </div>
</div>
```

**Data Attributes:**
- `data-name` - Product name (for filtering/sorting)
- `data-category` - Product category
- `data-volume` - Volume unit (L, g, kg, mL, u, etc.)
- `data-barcode` - EAN/UPC barcode
- `data-price` - Price (numeric, no currency symbol)

**Grid Columns Order:**
1. Product Name
2. Category
3. Barcode/EAN
4. Volume Unit
5. Price
6. Actions (View/Edit/Delete)

---

## 🏷️ Categories (categories.html)

### Search Input
```html
<input type="text" 
       id="searchInput" 
       class="search-input form-input-flex" 
       placeholder="Search categories...">
```
**ID**: `searchInput` - Bind search functionality

### Categories List Container
```html
<div class="list-container list-container-no-shadow" id="categoriesList">
    <!-- Category items go here -->
</div>
```
**Container ID**: `categoriesList` - Main list for all category items

### Individual Category Item Structure
```html
<div class="list-item list-item-compact">
    <div class="list-item-main categories-list-grid">
        <div class="category-color-box" style="background-color: #10b981;"></div>
        <div class="category-name">Dairy</div>
        <div class="category-meta">18 Items</div>
        <div class="category-meta">8.4%</div>
        <div style="color: var(--primary-color); font-weight: 500;">245.80 €</div>
        <div class="list-item-actions">
            <!-- Action buttons -->
        </div>
    </div>
</div>
```

**Important Notes:**
- Categories use `inline style` for `background-color` (dynamic per category)
- Color box is first column (32px fixed)
- No data attributes currently (can be added as needed)

**Grid Columns Order:**
1. Color Box (visual indicator)
2. Category Name
3. Item Count
4. Percentage
5. Total Amount
6. Actions (Edit/Delete)

### Category Chart
```html
<canvas id="categoryChart"></canvas>
```
**ID**: `categoryChart` - Bind Chart.js or similar library

---

## 🏪 Merchants (merchants.html)

### Search Input
```html
<input type="text" 
       id="searchInput" 
       class="search-input" 
       placeholder="Search merchants...">
```
**ID**: `searchInput` - Bind search functionality

### Merchants List Container
```html
<div class="list-container" id="merchantsList">
    <!-- Merchant items go here -->
</div>
```
**Container ID**: `merchantsList` - Main list for all merchant items

### Individual Merchant Item Structure
```html
<div class="list-item merchant-item" 
     data-name="Continente" 
     data-location="Faro Centro" 
     data-receipts="8" 
     data-spent="687.40">
    
    <div class="list-item-main merchants-list-grid">
        <div class="list-item-value">Continente</div>
        <div class="list-item-value">Faro Centro</div>
        <div class="list-item-value">8 receipts</div>
        <div class="list-item-value">687.40 €</div>
        <div class="list-item-actions">
            <!-- Action buttons -->
        </div>
    </div>
</div>
```

**Data Attributes:**
- `data-name` - Merchant name (for filtering/sorting)
- `data-location` - Merchant location
- `data-receipts` - Number of receipts (numeric)
- `data-spent` - Total amount spent (numeric, no currency symbol)

**Grid Columns Order:**
1. Merchant Name
2. Location
3. Total Receipts
4. Total Spent
5. Actions (View/Edit/Delete)

---

## 🧾 Receipt Detail (receipt-1001.html)

### Page Structure
```html
<h1 class="page-title">RCPT-2025-1001-CON</h1>
```
**Note:** Receipt code in page title (can be dynamic)

### Receipt Info Fields
All fields are **static displays** (read-only), no IDs needed for updating individual fields.
Structure is CSS-driven using classes:
- `.product-detail-layout` - Main card container
- `.product-info-item` - Individual info blocks
- `.product-info-label` - Field labels
- `.product-info-value` - Field values

### Item List Container
Items are hardcoded in the HTML. For dynamic loading, target the list container's parent `.list-container` div.

**Important:** Receipt detail pages are **visual guides only**. In production, these would be dynamically generated by backend.

---

## 🛒 Product Detail (product-2001.html)

### Photo Upload
```html
<img id="product-image" src="..." style="display: none;">
<div id="upload-area" class="file-upload">
    <input type="file" id="photo-upload" accept="image/*">
</div>
```

**IDs:**
- `product-image` - Image element (hidden until photo uploaded)
- `upload-area` - Upload placeholder div
- `photo-upload` - File input element

### Product Info Fields
Same structure as receipt detail - CSS-driven classes, no specific IDs for individual fields.

### Price History Chart
```html
<canvas id="priceHistoryChart" style="max-height: 250px;"></canvas>
```
**ID**: `priceHistoryChart` - Bind Chart.js for price trends

---

## 🏪 Merchant Detail (merchant-4001.html, merchant-4002.html)

### Photo Upload
```html
<input type="file" id="photo-upload" accept="image/*">
```
**ID**: `photo-upload` - File input for merchant logo/photo

### Spending Chart
```html
<canvas id="spendingChart"></canvas>
```
**ID**: `spendingChart` - Bind Chart.js for spending over time

### Category Breakdown Chart
```html
<canvas id="categoryChart"></canvas>
```
**ID**: `categoryChart` - Bind Chart.js for category distribution

---

## ➕ Add/Edit Forms

### Product Forms (product-add.html, product-edit-2001.html)
```html
<input type="file" id="product-photo" accept="image/*">
```
**ID**: `product-photo` - Product photo upload

### Common Pattern
All form inputs use standard HTML form elements with `name` attributes.  
No special IDs required beyond file uploads (already documented above).

**Form Submission**: Handle via JavaScript with `FormData` API or traditional form POST.

---

## 📊 Chart Elements

### Summary Table

| Page | Chart ID | Purpose | Library Suggested |
|------|----------|---------|-------------------|
| `categories.html` | `categoryChart` | Category spending pie/donut | Chart.js |
| `product-2001.html` | `priceHistoryChart` | Product price over time | Chart.js line |
| `merchant-4001.html` | `spendingChart` | Merchant spending over time | Chart.js line/bar |
| `merchant-4001.html` | `categoryChart` | Merchant category breakdown | Chart.js pie/donut |
| `merchant-4002.html` | `spendingChart` | Merchant spending over time | Chart.js line/bar |
| `merchant-4002.html` | `categoryChart` | Merchant category breakdown | Chart.js pie/donut |

**Chart.js CDN:**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

---

## 🔍 Search & Filter Elements

### All Search Inputs Share Same ID Pattern

| Page | ID | Placeholder Text |
|------|-----|------------------|
| `receipts.html` | `searchInput` | "Search receipts by merchant, date, or amount..." |
| `products.html` | `searchInput` | "Search products by name, category, or price..." |
| `categories.html` | `searchInput` | "Search categories..." |
| `merchants.html` | `searchInput` | "Search merchants by name, category, or location..." |

**Implementation Pattern:**
```javascript
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    // Filter logic using data attributes
});
```

---

## 📑 Quick Reference Tables

### Dashboard Data Binding

| ID | Data Field | Type | Example Value |
|----|-----------|------|---------------|
| `monthly-expenses` | `total-expenses` | Currency | "2,847.65 €" |
| `expenseComparison` | `expense-comparison` | Text | "+12.5% from last month" |
| `total-receipts` | `receipt-count` | Number | "28" |
| `receipts-comparison` | `receipt-comparison` | Text | "+5 from last month" |
| `products-purchased` | `product-count` | Number | "156" |
| `products-comparison` | `product-comparison` | Text | "+18 from last month" |
| `recent-receipts-list` | `data-max-items` | Number | "3" |

### List Container IDs

| Page | Container ID | Item Class | Purpose |
|------|-------------|------------|---------|
| `receipts.html` | `receiptsList` | `.receipt-item` | All receipts listing |
| `products.html` | `productsList` | `.product-item` | All products listing |
| `categories.html` | `categoriesList` | `.list-item` | All categories listing |
| `merchants.html` | `merchantsList` | `.merchant-item` | All merchants listing |
| `index.html` | `recent-receipts-list` | `.receipt-card` | Recent receipts (max 3) |

### Data Attribute Patterns

#### Receipts
```javascript
{
    "data-receipt-id": "1001",        // String: Unique ID
    "data-merchant": "Continente",    // String: Merchant name
    "data-date": "2025-11-10",        // String: ISO date
    "data-products": "12",            // String (numeric): Product count
    "data-total": "87.45"             // String (numeric): Total amount
}
```

#### Products
```javascript
{
    "data-name": "Milk Semi-Skimmed", // String: Product name
    "data-category": "Dairy",         // String: Category name
    "data-volume": "L",               // String: Unit (L, g, kg, mL, u)
    "data-barcode": "5600308532147",  // String: EAN/UPC
    "data-price": "0.89"              // String (numeric): Price
}
```

#### Merchants
```javascript
{
    "data-name": "Continente",        // String: Merchant name
    "data-location": "Faro Centro",   // String: Location
    "data-receipts": "8",             // String (numeric): Receipt count
    "data-spent": "687.40"            // String (numeric): Total spent
}
```

#### Receipt Cards (Dashboard)
```javascript
{
    "data-receipt-id": "1001",        // String: Unique receipt ID
    "data-merchant-id": "4001",       // String: Associated merchant ID
    "data-field": "merchant-name",    // String: Field identifier
    "data-field": "product-count",    // String: Field identifier
    "data-field": "receipt-date",     // String: Field identifier
    "data-field": "receipt-total"     // String: Field identifier
}
```

### Grid Class Patterns

| List Type | CSS Class | Column Template |
|-----------|-----------|----------------|
| Categories | `.categories-list-grid` | `32px 1fr 80px 70px 90px 80px` |
| Receipts | `.receipts-list-grid` | `1.2fr 2fr 1fr 0.8fr 0.8fr 180px` |
| Products | `.products-list-grid` | `2fr 1.5fr 1.2fr 1.5fr 1fr 180px` |
| Merchants | `.merchants-list-grid` | `2fr 1.5fr 1.2fr 1.2fr 180px` |
| Receipt Items | `.receipt-items-grid` | `2fr 1.2fr 1.5fr 0.8fr 0.8fr 0.6fr` |

---

## 🎯 Best Practices for Scripting

### 1. List Population
```javascript
// Example: Populate receipts list
function populateReceipts(receipts) {
    const container = document.getElementById('receiptsList');
    container.innerHTML = ''; // Clear existing
    
    receipts.forEach(receipt => {
        const item = document.createElement('div');
        item.className = 'list-item receipt-item';
        item.setAttribute('data-receipt-id', receipt.id);
        item.setAttribute('data-merchant', receipt.merchant);
        item.setAttribute('data-date', receipt.date);
        item.setAttribute('data-products', receipt.productCount);
        item.setAttribute('data-total', receipt.total);
        
        item.innerHTML = `
            <div class="list-item-main receipts-list-grid">
                <div class="list-item-value">${receipt.code}</div>
                <div class="list-item-value">${receipt.merchant}</div>
                <div class="list-item-value">${receipt.displayDate}</div>
                <div class="list-item-value">${receipt.productCount} items</div>
                <div class="list-item-value">${receipt.total} €</div>
                <div class="list-item-actions">
                    <a href="receipt-${receipt.id}.html" class="btn btn-secondary btn-sm">👁️</a>
                    <a href="receipt-edit-${receipt.id}.html" class="btn btn-secondary btn-sm">✏️</a>
                    <button class="btn btn-danger btn-sm">🗑️</button>
                </div>
            </div>
        `;
        
        container.appendChild(item);
    });
}
```

### 2. Search/Filter Implementation
```javascript
// Generic filter function
function filterList(containerId, searchTerm, attributes) {
    const items = document.querySelectorAll(`#${containerId} .list-item`);
    
    items.forEach(item => {
        const matches = attributes.some(attr => {
            const value = item.getAttribute(`data-${attr}`) || '';
            return value.toLowerCase().includes(searchTerm);
        });
        
        item.style.display = matches ? '' : 'none';
    });
}

// Example usage for receipts
document.getElementById('searchInput').addEventListener('input', (e) => {
    filterList('receiptsList', e.target.value.toLowerCase(), 
               ['merchant', 'date', 'total']);
});
```

### 3. Dashboard Stats Update
```javascript
// Update dashboard statistics
function updateDashboardStats(stats) {
    document.getElementById('monthly-expenses').textContent = 
        `${stats.monthlyExpenses.toFixed(2)} €`;
    
    document.getElementById('expenseComparison').textContent = 
        stats.expenseComparison;
    
    document.getElementById('total-receipts').textContent = 
        stats.receiptCount;
    
    document.getElementById('receipts-comparison').textContent = 
        stats.receiptsComparison;
    
    document.getElementById('products-purchased').textContent = 
        stats.productCount;
    
    document.getElementById('products-comparison').textContent = 
        stats.productsComparison;
}
```

### 4. Chart Initialization
```javascript
// Example: Initialize category chart
const ctx = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: categories.map(c => c.name),
        datasets: [{
            data: categories.map(c => c.amount),
            backgroundColor: categories.map(c => c.color)
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
```

### 5. Data Attribute Querying
```javascript
// Get all receipts from specific merchant
function getReceiptsByMerchant(merchantName) {
    return Array.from(document.querySelectorAll('.receipt-item'))
        .filter(item => item.getAttribute('data-merchant') === merchantName);
}

// Get products in price range
function getProductsInPriceRange(min, max) {
    return Array.from(document.querySelectorAll('.product-item'))
        .filter(item => {
            const price = parseFloat(item.getAttribute('data-price'));
            return price >= min && price <= max;
        });
}
```

---

## 📝 Notes & Recommendations

### ID Naming Convention
- **Containers**: Use plural form + "List" (e.g., `receiptsList`, `productsList`)
- **Singular items**: Use descriptive names (e.g., `monthly-expenses`, `searchInput`)
- **Charts**: Use purpose + "Chart" (e.g., `categoryChart`, `priceHistoryChart`)

### Data Attributes Convention
- **Identifiers**: `data-*-id` format (e.g., `data-receipt-id`, `data-merchant-id`)
- **Sortable fields**: Include in data attributes (e.g., `data-date`, `data-price`)
- **Filterable fields**: Include in data attributes (e.g., `data-merchant`, `data-category`)
- **Field identifiers**: Use `data-field` for dynamic content binding

### Missing IDs (Intentional)
The following elements **do not have IDs** by design:
- Individual form inputs (use `name` attributes instead)
- Static text displays in detail pages (use CSS classes for styling)
- Navigation elements (not meant for dynamic updates)
- Category color boxes (use inline styles for dynamic colors)

### Backend Integration Tips
1. **Use data attributes for sorting/filtering** - All list items have sortable fields
2. **Preserve grid classes** - When adding items dynamically, use the correct grid class
3. **Maintain HTML structure** - Follow the documented structure for consistency
4. **Currency formatting** - Backend should format numbers, HTML displays as text
5. **Date formatting** - Store ISO dates in data attributes, display formatted text

---

## 🚀 Quick Start Checklist

- [ ] Identify target page from table of contents
- [ ] Locate container ID (e.g., `receiptsList`, `productsList`)
- [ ] Review data attribute structure for that entity type
- [ ] Use appropriate grid class (`.receipts-list-grid`, etc.)
- [ ] Implement search using `searchInput` ID
- [ ] Initialize charts using canvas IDs
- [ ] Update dashboard stats using documented IDs
- [ ] Test filtering using data attributes
- [ ] Verify responsive behavior on mobile

---

## 📚 Additional Resources

- **CSS Documentation**: See `styles.css` for complete styling reference
- **Visual Guides**: Detail pages (product-2001.html, receipt-1001.html) show final layout
- **Grid Classes**: Defined in `styles.css` under "List & Table Components"
- **Data Flow**: Use data attributes → JavaScript logic → DOM updates

---

**End of Documentation**  
*For questions or issues, refer to the HTML source files or CSS for implementation details.*
