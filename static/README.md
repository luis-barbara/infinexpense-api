# InfinExpense - Frontend Application

**Modern expense tracking interface with modular architecture**

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Project Structure](#-project-structure)
4. [Quick Start](#-quick-start)
5. [Template System](#-template-system)
6. [CSS Architecture](#-css-architecture)
7. [JavaScript Modules](#-javascript-modules)
8. [Backend Integration](#-backend-integration)
9. [Development](#-development)
10. [Browser Support](#-browser-support)

---

## 🎯 Overview

InfinExpense is a complete frontend application for expense tracking with receipts, products, merchants, and categories. Built with **vanilla HTML, CSS, and JavaScript**, it features:

- **Modular CSS** architecture (16 separate modules)
- **Template system** for shared navigation
- **Dynamic data** loading with `data-*` attributes
- **Interactive charts** using Chart.js
- **Responsive design** for mobile/desktop
- **Clean separation** of concerns (no inline styles)

**Purpose**: This is a **static frontend** designed to integrate with a Python backend (Flask/Django). All dynamic content is loaded via JavaScript from API endpoints.

---

## ✨ Features

### Core Functionality
- ✅ **Dashboard** - Monthly statistics, recent receipts, expense trends
- ✅ **Receipts** - List, view, add, edit receipts with products
- ✅ **Products** - Track products, prices, purchase history
- ✅ **Categories** - Organize expenses by category with colors
- ✅ **Merchants** - Store locations, totals, maps integration

### Technical Features
- ✅ **Template System** - Single-source navigation that updates everywhere
- ✅ **Modular CSS** - 16 organized modules for easy maintenance
- ✅ **Pagination** - Client-side pagination on all list pages
- ✅ **Search & Filter** - Real-time filtering on lists
- ✅ **Charts** - Interactive visualizations (pie, line, bar)
- ✅ **File Upload** - Receipt and product photo uploads
- ✅ **Form Validation** - Ready for backend validation integration

---

## 📁 Project Structure

```
static/
├── index.html                 # Dashboard (main entry point)
│
├── category/                  # Category pages
│   ├── categories.html       # Category list with pie chart
│   ├── category-add.html     # Add new category
│   └── category-edit-*.html  # Edit category form
│
├── merchant/                  # Merchant pages
│   ├── merchants.html        # Merchant list
│   ├── merchant-*.html       # Merchant detail pages
│   ├── merchant-add.html     # Add new merchant
│   └── merchant-edit-*.html  # Edit merchant form
│
├── product/                   # Product pages
│   ├── products.html         # Product list
│   ├── product-*.html        # Product detail with price history
│   ├── product-add.html      # Add new product
│   └── product-edit-*.html   # Edit product form
│
├── receipt/                   # Receipt pages
│   ├── receipts.html         # Receipt list
│   ├── receipt-*.html        # Receipt detail with products
│   └── receipt-add.html      # Add new receipt
│
├── templates/                 # Reusable HTML templates
│   ├── header.html           # Navigation (single source of truth)
│   └── footer.html           # Footer placeholder
│
├── css/                       # Modular CSS files
│   ├── main.css              # Entry point (imports all modules)
│   ├── variables.css         # CSS custom properties
│   ├── reset.css             # Browser normalization
│   ├── layout.css            # Navigation, containers
│   ├── grids.css             # Grid layouts for lists
│   ├── cards.css             # Card components
│   ├── buttons.css           # Button styles
│   ├── forms.css             # Form inputs, labels
│   ├── lists.css             # List and table components
│   ├── details.css           # Detail page layouts
│   ├── charts.css            # Chart containers
│   ├── badges.css            # Badges and status indicators
│   ├── images.css            # Images and upload areas
│   ├── utilities.css         # Utility classes
│   ├── responsive.css        # Mobile styles
│   ├── animations.css        # Transitions
│   └── styles.css            # ⚠️ DEPRECATED - kept for reference
│
├── js/                        # JavaScript modules
│   ├── template-loader.js    # Template system (loads header/footer)
│   ├── dashboard.js          # Dashboard interactions
│   ├── receipts-list.js      # Receipt list pagination
│   ├── products-list.js      # Product list pagination
│   ├── merchants-list.js     # Merchant list pagination
│   ├── category-chart.js     # Category pie chart
│   ├── product-detail.js     # Product price history chart
│   └── merchant-detail.js    # Merchant spending chart
│
└── docs/                      # Documentation
    ├── SCRIPTING_IDS_REFERENCE.md   # All IDs and data-* attributes
    └── BACKEND_INTEGRATION.md       # Backend integration guide
```

---

## 🚀 Quick Start

### 1. Serve the Application

You need a local web server (templates won't load from `file://`):

**Option A: Python**
```bash
cd static
python3 -m http.server 8000
```
Then open: http://localhost:8000/index.html

**Option B: Node.js (with live-server)**
```bash
npm install -g live-server
cd static
live-server --port=8000
```

**Option C: VS Code Live Server Extension**
1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"

### 2. Navigate the Application

- **Dashboard**: http://localhost:8000/index.html
- **Receipts**: http://localhost:8000/receipt/receipts.html
- **Products**: http://localhost:8000/product/products.html
- **Categories**: http://localhost:8000/category/categories.html
- **Merchants**: http://localhost:8000/merchant/merchants.html

### 3. Test Key Features

1. Click navigation links (header loads dynamically)
2. Try pagination on list pages
3. Use search/filter on lists
4. View charts on dashboard and category pages
5. Check responsive design (resize browser)

---

## 🎨 Template System

The navigation header is **loaded dynamically** via JavaScript, allowing you to edit it once and update all pages.

### How It Works

1. **Template File**: `templates/header.html` contains the navigation
2. **Loader Script**: `js/template-loader.js` fetches and injects it
3. **Placeholder**: Each page has `<div data-template="header"></div>`

### Template Structure

```html
<!-- templates/header.html -->
<nav class="navbar">
    <div class="nav-container">
        <a href="{BASE_PATH}index.html" class="nav-brand">InfinExpense</a>
        <ul class="nav-menu">
            <li><a href="{BASE_PATH}index.html" class="nav-link" data-page="dashboard">Dashboard</a></li>
            <li><a href="{BASE_PATH}receipt/receipts.html" class="nav-link" data-page="receipts">Receipts</a></li>
            <!-- More links... -->
        </ul>
    </div>
</nav>
```

**Key Features:**
- `{BASE_PATH}` placeholder is replaced with `../` based on page depth
- `data-page` attributes enable active link highlighting
- Works from root and subdirectories automatically

### How To Use

**In every HTML page:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title - InfinExpense</title>
    <link rel="stylesheet" href="css/main.css">  <!-- Root level -->
    <!-- OR -->
    <link rel="stylesheet" href="../css/main.css">  <!-- Subdirectory -->
</head>
<body data-active-page="dashboard">  <!-- Highlights active nav link -->
    
    <!-- Navigation Template -->
    <div data-template="header"></div>
    <script src="js/template-loader.js"></script>  <!-- Loads right after template div -->
    
    <!-- Your page content -->
    <div class="container">
        <!-- Content here -->
    </div>
    
</body>
</html>
```

### Changing the Navigation

To update navigation **on all pages**:

1. Edit `templates/header.html`
2. Reload any page
3. Changes appear everywhere automatically ✨

---

## 🎨 CSS Architecture

### Module Organization

The CSS is split into **16 logical modules** for easy maintenance:

```
css/main.css              ← Load this in your HTML
    ├── variables.css     ← Colors, spacing, fonts (47 CSS custom properties)
    ├── reset.css         ← Browser normalization
    ├── layout.css        ← Navigation, containers, page structure
    ├── grids.css         ← 5 grid layouts for different list types
    ├── cards.css         ← Card components
    ├── buttons.css       ← Button variants (primary, secondary, danger)
    ├── forms.css         ← Form inputs, labels, file uploads
    ├── lists.css         ← Lists and tables
    ├── details.css       ← Detail page layouts
    ├── charts.css        ← Chart container styles
    ├── badges.css        ← Badges and status indicators
    ├── images.css        ← Images and upload areas
    ├── utilities.css     ← Utility classes (50+ helpers)
    ├── responsive.css    ← Mobile breakpoints
    └── animations.css    ← Transitions and effects
```

### How To Use

**1. Link to main.css in your HTML:**

```html
<link rel="stylesheet" href="css/main.css">
```

The `main.css` file imports all modules in the correct order.

**2. Edit specific modules:**

- Need to change colors? → `css/variables.css`
- Change button styles? → `css/buttons.css`
- Update form inputs? → `css/forms.css`
- Add utility class? → `css/utilities.css`

**3. No inline styles:**

All styles use classes. Category colors are the **only exception** (dynamic from database).

### CSS Custom Properties (Variables)

All colors, spacing, and fonts are centralized in `variables.css`:

```css
/* Example from variables.css */
:root {
    /* Colors */
    --primary-color: #4169E1;
    --success-color: #10b981;
    --danger-color: #ef4444;
    
    /* Spacing */
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    
    /* Typography */
    --font-family: 'Inter', -apple-system, sans-serif;
    --font-size-base: 1rem;
    
    /* And 40 more... */
}
```

**To change the color scheme**, just edit these variables!

### Utility Classes

Over **50 utility classes** for common patterns:

```css
/* Flexbox */
.flex, .flex-col, .flex-center, .flex-between

/* Text */
.text-center, .text-right, .text-primary-color

/* Spacing */
.mb-lg, .mt-2, .mx-auto

/* Width */
.max-width-800, .width-300

/* Display */
.hidden, .block, .cursor-pointer

/* And many more in utilities.css */
```

---

## 📜 JavaScript Modules

### Template Loader (`js/template-loader.js`)

**Purpose**: Loads navigation header dynamically  
**Features**:
- Auto-detects page depth
- Calculates correct `../` path
- Replaces `{BASE_PATH}` placeholder
- Highlights active navigation link

**No configuration needed** - works automatically!

### Page-Specific Modules

#### `dashboard.js`
- **Used by**: `index.html`
- **Features**: Toggle expense comparison mode, load recent receipts

#### `receipts-list.js`
- **Used by**: `receipt/receipts.html`
- **Features**: Pagination, search/filter receipts

#### `products-list.js`
- **Used by**: `product/products.html`
- **Features**: Pagination, search/filter products

#### `merchants-list.js`
- **Used by**: `merchant/merchants.html`
- **Features**: Pagination, search/filter merchants

#### `category-chart.js`
- **Used by**: `category/categories.html`
- **Features**: Renders pie chart of spending by category

#### `product-detail.js`
- **Used by**: `product/product-*.html`
- **Features**: Price history line chart

#### `merchant-detail.js`
- **Used by**: `merchant/merchant-*.html`
- **Features**: Spending trends bar chart

### How To Add JavaScript

```html
<!-- At end of body, after content -->
<script src="../js/template-loader.js"></script>
<script src="../js/receipts-list.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>  <!-- If using charts -->
```

---

## 🔌 Backend Integration

See **[docs/BACKEND_INTEGRATION.md](docs/BACKEND_INTEGRATION.md)** for complete integration guide.

### Quick Overview

**1. Data Attributes**

All dynamic content uses `data-*` attributes:

```html
<!-- Example: Receipt item -->
<div class="list-item" data-receipt-id="1001">
    <span data-field="merchant-name">Continente</span>
    <span data-field="receipt-date">Nov 10, 2025</span>
    <span data-field="receipt-total">87.45 €</span>
</div>
```

**2. JavaScript Integration Points**

Your backend should provide JSON data that JavaScript uses to:
- Populate `data-field` elements
- Render charts
- Fill forms
- Update statistics

**3. Example API Response**

```json
{
    "receipt_id": 1001,
    "merchant_name": "Continente",
    "date": "2025-11-10",
    "total": 87.45,
    "products": [
        {"id": 2001, "name": "Milk", "price": 1.20}
    ]
}
```

**4. Server-Side Templates (Optional)**

Instead of JavaScript template loader, you can use Flask/Django templates:

```html
<!-- Flask/Jinja2 Example -->
{% include 'header.html' %}

<!-- Django Example -->
{% include "header.html" %}
```

Then remove `<script src="js/template-loader.js"></script>` from pages.

### Key Integration Files

- **docs/SCRIPTING_IDS_REFERENCE.md** - All IDs and data attributes
- **docs/BACKEND_INTEGRATION.md** - Flask/Django examples, API design

---

## 🛠️ Development

### Editing the Application

**To edit navigation:**
```bash
# Edit this file:
templates/header.html

# Changes apply to all pages automatically
```

**To edit styles:**
```bash
# Colors, spacing, fonts:
css/variables.css

# Buttons:
css/buttons.css

# Forms:
css/forms.css

# Utility classes:
css/utilities.css
```

**To edit page layout:**
```bash
# Edit specific HTML file:
product/products.html

# Or edit shared template:
templates/header.html
```

### Adding a New Page

1. **Create HTML file** (copy existing page as template)
2. **Add to navigation** in `templates/header.html`:
   ```html
   <li><a href="{BASE_PATH}newpage/page.html" class="nav-link" data-page="newpage">New Page</a></li>
   ```
3. **Set active page** in new page's `<body>`:
   ```html
   <body data-active-page="newpage">
   ```
4. **Add JavaScript** if needed in `js/` directory

### Testing

**Manual Testing:**
1. Start local server (see Quick Start)
2. Test navigation (all links work?)
3. Test responsive design (resize browser)
4. Test JavaScript features (pagination, charts, search)
5. Check console for errors (F12 → Console)

**What To Test:**
- ✅ Navigation loads on all pages
- ✅ Active link highlights correctly
- ✅ All links go to correct pages
- ✅ CSS loads properly (no broken styles)
- ✅ JavaScript runs without errors
- ✅ Charts render correctly
- ✅ Forms work (validation, submission)
- ✅ Search/filter functions work
- ✅ Pagination displays correct items

---

## 🌐 Browser Support

### Supported Browsers

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

### Required Features

The application uses modern web features:
- **CSS Grid** and **Flexbox**
- **CSS Custom Properties** (variables)
- **Fetch API** (template loader)
- **ES6 JavaScript** (arrow functions, const/let)
- **Chart.js** (v4.x)

### Fallbacks

- Template loader gracefully fails if fetch is unsupported
- CSS Grid falls back to flexbox on older browsers
- No IE11 support (uses modern JavaScript)

---

## 📝 Notes

### Category Colors

Category color boxes use **inline styles** intentionally:

```html
<div class="category-color-box" style="background-color: #10b981;"></div>
```

**Why?** These colors come from the database and are dynamic. This is the **only acceptable inline style** in the project.

### File Naming Convention

- **List pages**: `[entity]s.html` (plural) - e.g., `receipts.html`, `products.html`
- **Detail pages**: `[entity]-[id].html` - e.g., `receipt-1001.html`, `product-2001.html`
- **Form pages**: `[entity]-add.html`, `[entity]-edit-[id].html`

### IDs and Classes

- **IDs**: Unique per page, for JavaScript targeting
- **Classes**: Reusable, for styling
- **data-* attributes**: For backend integration and JavaScript logic

### Performance

- Template loader caches templates (one request per session)
- CSS is modular but loaded as single file (via @import)
- JavaScript modules are independent (no dependencies)
- Images should be lazy-loaded (to add)

---

## 🤝 Contributing

When adding features:

1. **Follow the modular structure** (keep CSS in modules, JS in separate files)
2. **No inline styles** (except category colors from database)
3. **Use utility classes** when possible
4. **Add data-* attributes** for backend integration
5. **Update documentation** if you add new IDs or data attributes
6. **Test in multiple browsers**

---

## 📚 Additional Resources

- **[docs/BACKEND_INTEGRATION.md](docs/BACKEND_INTEGRATION.md)** - Complete backend integration guide
- **[docs/SCRIPTING_IDS_REFERENCE.md](docs/SCRIPTING_IDS_REFERENCE.md)** - All IDs and data attributes

---

## 📄 License

This project is part of the InfinExpense expense tracking system.

---

**Built with ❤️ using vanilla HTML, CSS, and JavaScript**
