# Backend Integration Guide

This document provides comprehensive information for integrating the InfinExpense frontend with a Python/Flask backend and database.

## Table of Contents
1. [Data Attribute Convention](#data-attribute-convention)
2. [JavaScript Functions Reference](#javascript-functions-reference)
3. [Database Schema Mapping](#database-schema-mapping)
4. [Python Integration Examples](#python-integration-examples)
5. [API Endpoints Reference](#api-endpoints-reference)

---

## Data Attribute Convention

All dynamic HTML elements use `data-*` attributes to facilitate backend data binding.

### Receipts (`receipts.html`, `index.html`)

```html
<a href="receipt-1001.html" 
   class="list-item receipt-item" 
   data-receipt-id="1001" 
   data-merchant-id="4001">
    <!-- Receipt content -->
</a>
```

**Attributes:**
- `data-receipt-id`: Primary key from `receipts` table
- `data-merchant-id`: Foreign key to `merchants` table
- `data-field="merchant-name"`: Merchant name display element
- `data-field="receipt-date"`: Receipt date display
- `data-field="receipt-total"`: Total amount display
- `data-field="product-count"`: Number of products in receipt

### Products (`products.html`, `product-2001.html`)

```html
<div class="list-item product-item" 
     data-product-id="2001" 
     data-category-id="3001">
    <!-- Product content -->
</div>
```

**Attributes:**
- `data-product-id`: Primary key from `products` table
- `data-category-id`: Foreign key to `categories` table
- `data-field="product-name"`: Product name display
- `data-field="product-price"`: Current price display
- `data-field="category-name"`: Category name display

### Categories (`categories.html`)

```html
<div class="list-item category-item" 
     data-category-id="3001" 
     data-color="#4169E1">
    <!-- Category content -->
</div>
```

**Attributes:**
- `data-category-id`: Primary key from `categories` table
- `data-color`: Hex color code for visualization
- `data-field="category-name"`: Category name display
- `data-field="spending-total"`: Total spending in category

### Merchants (`merchants.html`)

```html
<div class="list-item merchant-item" 
     data-merchant-id="4001">
    <!-- Merchant content -->
</div>
```

**Attributes:**
- `data-merchant-id`: Primary key from `merchants` table
- `data-field="merchant-name"`: Merchant name display
- `data-field="receipt-count"`: Number of receipts from this merchant

---

## JavaScript Functions Reference

### Pagination System (receipts.html, products.html, merchants.html)

All list pages use the same pagination pattern:

#### `showPage(page)`
**Purpose:** Display items for a specific page number  
**Parameters:**
- `page` (number): Page number to display (1-indexed)

**Usage:**
```javascript
showPage(1); // Show first page
showPage(3); // Show third page
```

**Backend Integration:**
When fetching paginated data from backend:
```javascript
fetch(`/api/receipts?page=${page}&per_page=${itemsPerPage}`)
    .then(response => response.json())
    .then(data => {
        // Populate receipt list
        renderReceipts(data.items);
        totalItems = data.total;
        updatePagination();
    });
```

#### `updatePagination()`
**Purpose:** Update pagination controls and button states  
**Parameters:** None  
**Side Effects:** 
- Creates numbered page buttons
- Disables prev/next buttons at boundaries
- Highlights current page

#### `changePage(direction)`
**Purpose:** Navigate to previous or next page  
**Parameters:**
- `direction` (number): -1 for previous, +1 for next

**Usage:**
```html
<button onclick="changePage(-1)">Previous</button>
<button onclick="changePage(1)">Next</button>
```

#### `changeItemsPerPage()`
**Purpose:** Change number of items displayed per page  
**Triggers:** Dropdown selection change  
**Side Effects:** Resets to page 1

**HTML:**
```html
<select id="itemsPerPage" onchange="changeItemsPerPage()">
    <option value="5" selected>Show 5</option>
    <option value="10">Show 10</option>
    <option value="20">Show 20</option>
</select>
```

#### `filterItems()`
**Purpose:** Search/filter items based on text input  
**Parameters:** None (reads from `#searchInput`)  
**Data Attributes Set:** `data-visible="true|false"` on each item

**Usage:**
```html
<input type="text" id="searchInput" placeholder="Search...">
<button onclick="filterItems()">Search</button>
```

---

### Dashboard Functions (index.html)

#### `toggleComparisonMode()`
**Purpose:** Toggle between percentage and absolute value for expense comparison  
**Parameters:** None  
**Displays:** "+12.5%" ↔ "+€314.52"

**Backend Data Needed:**
```javascript
const lastMonthExpense = 2533.13; // From: SELECT SUM(total) FROM receipts WHERE month = last_month
const currentExpense = 2847.65;   // From: SELECT SUM(total) FROM receipts WHERE month = current_month
```

---

### Receipt Editing Functions (receipt-1001.html)

#### `updateProduct(input)`
**Purpose:** Update product amount or price and recalculate total  
**Parameters:**
- `input` (HTMLInputElement): The input element that changed

**HTML:**
```html
<input type="number" value="2" onchange="updateProduct(this)" data-product-id="2001">
<input type="number" value="0.89" onchange="updateProduct(this)" data-product-id="2001">
```

**Backend Integration:**
```javascript
function updateProduct(input) {
    const productId = input.getAttribute('data-product-id');
    const newValue = input.value;
    const fieldType = input.getAttribute('data-field'); // 'amount' or 'price'
    
    // Send to backend
    fetch(`/api/receipt-items/${productId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ [fieldType]: newValue })
    });
    
    calculateTotal();
}
```

#### `removeProduct(button)`
**Purpose:** Remove a product from the receipt  
**Parameters:**
- `button` (HTMLButtonElement): The remove button clicked

**HTML:**
```html
<button onclick="removeProduct(this)" data-product-id="2001">Remove</button>
```

**Backend Integration:**
```javascript
function removeProduct(button) {
    const productId = button.getAttribute('data-product-id');
    
    // Send to backend
    fetch(`/api/receipt-items/${productId}`, {
        method: 'DELETE'
    }).then(() => {
        // Remove from DOM
        button.closest('.product-row').remove();
        calculateTotal();
    });
}
```

#### `calculateTotal()`
**Purpose:** Recalculate receipt total based on all products  
**Parameters:** None  
**Updates:** Total display and product count

---

### Chart.js Integration

#### Category Pie Chart (categories.html)

```javascript
const categoryChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Dairy', 'Bakery', 'Meat', ...], // From categories table
        datasets: [{
            data: [450.50, 320.75, 890.20, ...],   // Spending per category
            backgroundColor: ['#4169E1', '#32CD32', ...] // From categories.color
        }]
    }
});
```

**Backend Data Structure:**
```python
@app.route('/api/categories/spending')
def get_category_spending():
    categories = db.execute("""
        SELECT c.id, c.name, c.color, SUM(ri.amount * ri.price) as total_spending
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id
        LEFT JOIN receipt_items ri ON ri.product_id = p.id
        GROUP BY c.id, c.name, c.color
    """)
    return jsonify(categories)
```

#### Price History Line Chart (product-2001.html)

```javascript
const priceChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['2025-11-01', '2025-11-05', ...],  // Dates
        datasets: [{
            label: 'Price',
            data: [0.89, 0.85, 0.92, ...],          // Prices over time
            borderColor: '#2563eb'
        }]
    }
});
```

**Backend Data Structure:**
```python
@app.route('/api/products/<int:product_id>/price-history')
def get_price_history(product_id):
    history = db.execute("""
        SELECT r.date, ri.price
        FROM receipt_items ri
        JOIN receipts r ON r.id = ri.receipt_id
        WHERE ri.product_id = ?
        ORDER BY r.date
    """, product_id)
    return jsonify(history)
```

---

## Database Schema Mapping

### Recommended Schema

```sql
-- Merchants Table
CREATE TABLE merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT DEFAULT '#6366f1', -- Hex color for charts
    icon TEXT, -- Optional emoji or icon
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Receipts Table
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER NOT NULL,
    date DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    image_path TEXT, -- Path to receipt image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id)
);

-- Products Table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Receipt Items Table (junction table with additional data)
CREATE TABLE receipt_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    amount DECIMAL(10,3) NOT NULL, -- Quantity (can be fractional for kg)
    price DECIMAL(10,2) NOT NULL,  -- Price per unit at time of purchase
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (amount * price) STORED,
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Indexes for performance
CREATE INDEX idx_receipts_merchant ON receipts(merchant_id);
CREATE INDEX idx_receipts_date ON receipts(date);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_receipt_items_receipt ON receipt_items(receipt_id);
CREATE INDEX idx_receipt_items_product ON receipt_items(product_id);
```

---

## Python Integration Examples

### Flask Application Structure

```python
from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'infinexpense.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

### Route: Dashboard
@app.route('/')
def dashboard():
    db = get_db()
    
    # Get current month stats
    stats = db.execute("""
        SELECT 
            COUNT(*) as total_receipts,
            SUM(total) as monthly_expenses,
            SUM((SELECT COUNT(*) FROM receipt_items WHERE receipt_id = receipts.id)) as products_purchased
        FROM receipts
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """).fetchone()
    
    # Get recent receipts
    recent_receipts = db.execute("""
        SELECT 
            r.id,
            r.date,
            r.total,
            m.id as merchant_id,
            m.name as merchant_name,
            COUNT(ri.id) as product_count
        FROM receipts r
        JOIN merchants m ON m.id = r.merchant_id
        LEFT JOIN receipt_items ri ON ri.receipt_id = r.id
        GROUP BY r.id
        ORDER BY r.date DESC
        LIMIT 3
    """).fetchall()
    
    return render_template('index.html', stats=stats, receipts=recent_receipts)

### Route: Receipts List with Pagination
@app.route('/receipts')
def receipts_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '')
    
    db = get_db()
    
    # Build query with search
    query = """
        SELECT 
            r.id,
            r.date,
            r.total,
            m.id as merchant_id,
            m.name as merchant_name,
            COUNT(ri.id) as product_count
        FROM receipts r
        JOIN merchants m ON m.id = r.merchant_id
        LEFT JOIN receipt_items ri ON ri.receipt_id = r.id
    """
    
    if search:
        query += " WHERE m.name LIKE ? OR r.date LIKE ? OR r.total LIKE ?"
        params = [f'%{search}%', f'%{search}%', f'%{search}%']
        receipts = db.execute(query + " GROUP BY r.id ORDER BY r.date DESC", params).fetchall()
    else:
        offset = (page - 1) * per_page
        receipts = db.execute(
            query + " GROUP BY r.id ORDER BY r.date DESC LIMIT ? OFFSET ?",
            [per_page, offset]
        ).fetchall()
    
    total = db.execute("SELECT COUNT(*) as count FROM receipts").fetchone()['count']
    
    return render_template('receipts.html', 
                          receipts=receipts, 
                          total=total, 
                          page=page, 
                          per_page=per_page)

### Route: Receipt Detail
@app.route('/receipt/<int:receipt_id>')
def receipt_detail(receipt_id):
    db = get_db()
    
    receipt = db.execute("""
        SELECT r.*, m.name as merchant_name
        FROM receipts r
        JOIN merchants m ON m.id = r.merchant_id
        WHERE r.id = ?
    """, [receipt_id]).fetchone()
    
    items = db.execute("""
        SELECT 
            ri.*,
            p.name as product_name,
            c.name as category_name
        FROM receipt_items ri
        JOIN products p ON p.id = ri.product_id
        JOIN categories c ON c.id = p.category_id
        WHERE ri.receipt_id = ?
    """, [receipt_id]).fetchall()
    
    return render_template('receipt-detail.html', receipt=receipt, items=items)

### API: Update Receipt Item
@app.route('/api/receipt-items/<int:item_id>', methods=['PATCH'])
def update_receipt_item(item_id):
    data = request.json
    db = get_db()
    
    # Update amount or price
    if 'amount' in data:
        db.execute("UPDATE receipt_items SET amount = ? WHERE id = ?", 
                  [data['amount'], item_id])
    if 'price' in data:
        db.execute("UPDATE receipt_items SET price = ? WHERE id = ?", 
                  [data['price'], item_id])
    
    db.commit()
    
    # Recalculate receipt total
    item = db.execute("SELECT receipt_id FROM receipt_items WHERE id = ?", 
                     [item_id]).fetchone()
    new_total = db.execute("""
        SELECT SUM(amount * price) as total 
        FROM receipt_items 
        WHERE receipt_id = ?
    """, [item['receipt_id']]).fetchone()['total']
    
    db.execute("UPDATE receipts SET total = ? WHERE id = ?", 
              [new_total, item['receipt_id']])
    db.commit()
    
    return jsonify({'success': True, 'new_total': new_total})

### API: Delete Receipt Item
@app.route('/api/receipt-items/<int:item_id>', methods=['DELETE'])
def delete_receipt_item(item_id):
    db = get_db()
    
    # Get receipt_id before deleting
    item = db.execute("SELECT receipt_id FROM receipt_items WHERE id = ?", 
                     [item_id]).fetchone()
    receipt_id = item['receipt_id']
    
    # Delete item
    db.execute("DELETE FROM receipt_items WHERE id = ?", [item_id])
    db.commit()
    
    # Recalculate receipt total
    new_total = db.execute("""
        SELECT SUM(amount * price) as total 
        FROM receipt_items 
        WHERE receipt_id = ?
    """, [receipt_id]).fetchone()['total'] or 0
    
    db.execute("UPDATE receipts SET total = ? WHERE id = ?", 
              [new_total, receipt_id])
    db.commit()
    
    return jsonify({'success': True, 'new_total': new_total})

### API: Category Spending Data for Chart
@app.route('/api/categories/spending')
def category_spending():
    db = get_db()
    
    data = db.execute("""
        SELECT 
            c.id,
            c.name,
            c.color,
            COALESCE(SUM(ri.amount * ri.price), 0) as spending
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id
        LEFT JOIN receipt_items ri ON ri.product_id = p.id
        GROUP BY c.id, c.name, c.color
        ORDER BY spending DESC
    """).fetchall()
    
    return jsonify([dict(row) for row in data])

### API: Product Price History for Chart
@app.route('/api/products/<int:product_id>/price-history')
def product_price_history(product_id):
    db = get_db()
    
    history = db.execute("""
        SELECT 
            r.date,
            ri.price
        FROM receipt_items ri
        JOIN receipts r ON r.id = ri.receipt_id
        WHERE ri.product_id = ?
        ORDER BY r.date
    """, [product_id]).fetchall()
    
    return jsonify([{'date': row['date'], 'price': row['price']} for row in history])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## API Endpoints Reference

### GET Endpoints

| Endpoint | Purpose | Query Parameters | Response |
|----------|---------|------------------|----------|
| `/` | Dashboard page | None | HTML |
| `/receipts` | Receipts list | `page`, `per_page`, `search` | HTML |
| `/receipt/<id>` | Receipt detail | None | HTML |
| `/products` | Products list | `page`, `per_page`, `search` | HTML |
| `/product/<id>` | Product detail | None | HTML |
| `/categories` | Categories list | None | HTML |
| `/merchants` | Merchants list | `page`, `per_page`, `search` | HTML |
| `/api/categories/spending` | Category spending data | None | JSON |
| `/api/products/<id>/price-history` | Product price history | None | JSON |

### POST Endpoints

| Endpoint | Purpose | Body Parameters | Response |
|----------|---------|-----------------|----------|
| `/api/receipts` | Create receipt | `merchant_id`, `date`, `total`, `items[]` | JSON |
| `/api/products` | Create product | `name`, `category_id`, `description` | JSON |
| `/api/categories` | Create category | `name`, `color`, `icon` | JSON |
| `/api/merchants` | Create merchant | `name`, `location` | JSON |

### PATCH Endpoints

| Endpoint | Purpose | Body Parameters | Response |
|----------|---------|-----------------|----------|
| `/api/receipt-items/<id>` | Update receipt item | `amount`, `price` | JSON |
| `/api/products/<id>` | Update product | `name`, `category_id`, `description` | JSON |
| `/api/categories/<id>` | Update category | `name`, `color`, `icon` | JSON |
| `/api/merchants/<id>` | Update merchant | `name`, `location` | JSON |

### DELETE Endpoints

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `/api/receipt-items/<id>` | Delete receipt item | JSON |
| `/api/receipts/<id>` | Delete receipt | JSON |
| `/api/products/<id>` | Delete product | JSON |
| `/api/categories/<id>` | Delete category | JSON |
| `/api/merchants/<id>` | Delete merchant | JSON |

---

## Form Submission Examples

### Add Receipt Form (receipt-add.html)

```html
<form id="addReceiptForm" method="POST" action="/api/receipts">
    <select name="merchant_id" data-field="merchant-id" required>
        <!-- Populated from merchants table -->
    </select>
    
    <input type="date" name="date" data-field="receipt-date" required>
    
    <input type="file" name="image" accept="image/*" data-field="receipt-image">
    
    <!-- Dynamic product selection -->
    <div id="productsList" data-container="products">
        <!-- JavaScript adds product rows here -->
    </div>
    
    <button type="submit">Add Receipt</button>
</form>
```

**JavaScript Submission:**
```javascript
document.getElementById('addReceiptForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/api/receipts', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/receipt/${data.receipt_id}`;
        }
    });
});
```

---

## Data Population Template

Use this Python script to populate HTML templates with database data:

```python
from jinja2 import Template

def render_receipt_list_items(receipts):
    """Render receipt list items with data attributes"""
    template = Template('''
    {% for receipt in receipts %}
    <a href="receipt-{{ receipt.id }}.html" 
       class="list-item receipt-item" 
       data-receipt-id="{{ receipt.id }}" 
       data-merchant-id="{{ receipt.merchant_id }}">
        <div class="list-item-main">
            <div>
                <div class="list-item-label">Receipt ID</div>
                <div class="list-item-value" data-field="receipt-id">#{{ receipt.id }}</div>
            </div>
            <div>
                <div class="list-item-label">Merchant</div>
                <div class="list-item-value" data-field="merchant-name">{{ receipt.merchant_name }}</div>
            </div>
            <div>
                <div class="list-item-label">Date</div>
                <div class="list-item-value" data-field="receipt-date">{{ receipt.date }}</div>
            </div>
            <div>
                <div class="list-item-label">Products</div>
                <div class="list-item-value" data-field="product-count">{{ receipt.product_count }} items</div>
            </div>
            <div>
                <div class="list-item-label">Total</div>
                <div class="list-item-value" data-field="receipt-total">€{{ "%.2f"|format(receipt.total) }}</div>
            </div>
        </div>
    </a>
    {% endfor %}
    ''')
    
    return template.render(receipts=receipts)
```

---

## Security Considerations

1. **Input Validation**: Always validate and sanitize user inputs server-side
2. **SQL Injection**: Use parameterized queries (shown in examples)
3. **CSRF Protection**: Add CSRF tokens to all forms
4. **Authentication**: Implement user authentication for production
5. **File Uploads**: Validate file types and sizes for receipt images
6. **XSS Prevention**: Escape HTML output when rendering user data

---

## Testing Checklist

- [ ] Test pagination with different page sizes (5, 10, 20, 50)
- [ ] Test search functionality across all list pages
- [ ] Test receipt item editing (amount and price changes)
- [ ] Test receipt item deletion
- [ ] Test total recalculation after edits
- [ ] Test form submissions (add receipt, product, category, merchant)
- [ ] Test Chart.js data loading from API
- [ ] Test responsive design on mobile devices
- [ ] Test data attribute presence on all dynamic elements
- [ ] Test SQL queries for performance with large datasets

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**For Questions**: Refer to main README.md or contact project maintainer
