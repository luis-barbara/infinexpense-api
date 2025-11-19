# InfinExpense - API Integration Guide

**Version:** 1.0  
**Last Updated:** November 14, 2025  
**Audience:** Backend Developers, Full-Stack Developers

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Getting Started](#getting-started)
4. [Data Models & Relationships](#data-models--relationships)
5. [API Endpoints Reference](#api-endpoints-reference)
6. [Frontend Integration](#frontend-integration)
7. [Complete Workflow Examples](#complete-workflow-examples)
8. [HTML Structure Guide](#html-structure-guide)
9. [CSS Classes Reference](#css-classes-reference)
10. [JavaScript Integration](#javascript-integration)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

InfinExpense is a receipt and expense tracking application with a modern, component-based frontend architecture. This guide will help you integrate the frontend with your backend API, implement CRUD operations, and maintain data relationships between merchants, products, receipts, and categories.

### Key Features
- **Merchant Management**: Store information, locations, and track receipt history
- **Product Catalog**: Track products with prices, categories, and barcodes
- **Receipt Processing**: Link receipts to merchants with itemized product lists
- **Category System**: Organize products into categorized groups
- **Automatic Calculations**: Sum totals from product lists dynamically

### Technology Stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **CSS Architecture**: Modular CSS with utility classes
- **JavaScript**: Event-driven, data-attribute based interactions
- **Backend**: Your API (REST recommended)
- **Data Format**: JSON

---

## System Architecture

### Frontend Structure
```
static/
├── index.html                  # Dashboard/Home
├── css/                        # Modular stylesheets
│   ├── main.css               # Main entry point (imports all CSS)
│   ├── components-extended.css # Extended components
│   ├── forms.css              # Form styling
│   └── ...
├── js/                         # JavaScript modules
│   ├── template-loader.js     # Navigation template
│   ├── receipt-edit.js        # Receipt edit functionality
│   └── ...
├── merchant/                   # Merchant pages
│   ├── list.html
│   ├── view-example.html
│   ├── add.html
│   └── edit-example.html
├── product/                    # Product pages
│   ├── list.html
│   ├── view-example.html
│   ├── add.html
│   └── edit-example.html
├── receipt/                    # Receipt pages
│   ├── list.html
│   ├── view-example.html
│   ├── add.html
│   └── edit-example.html
└── category/                   # Category pages
    ├── list.html
    ├── view-example.html
    ├── add.html
    └── edit-example.html
```

### Page Naming Convention
Each entity follows a consistent naming pattern:
- `list.html` - List all items (table/grid view)
- `view-example.html` - View single item details (read-only)
- `add.html` - Create new item form
- `edit-example.html` - Edit existing item form

---

## Getting Started

### Prerequisites
1. **Backend API** running and accessible
2. **CORS** configured to allow frontend domain
3. **JSON** responses from all API endpoints
4. **RESTful** endpoint structure (recommended)

### Quick Start Checklist
- [ ] Clone/download the static frontend files
- [ ] Configure API base URL in your JavaScript
- [ ] Test API connectivity
- [ ] Implement authentication if required
- [ ] Start with Merchant → Product → Receipt workflow

### Initial Setup

1. **Configure API Base URL**
   Create a configuration file: `js/config.js`
   ```javascript
   // js/config.js
   const API_CONFIG = {
       baseURL: 'http://localhost:8000/api', // Change to your API URL
       timeout: 10000,
       headers: {
           'Content-Type': 'application/json',
           // Add authentication headers if needed
           // 'Authorization': 'Bearer YOUR_TOKEN'
       }
   };
   ```

2. **Include Config in HTML**
   Add to the `<head>` section of each page:
   ```html
   <script src="../js/config.js"></script>
   ```

---

## Data Models & Relationships

Understanding the data structure is crucial for proper integration.

### Entity Relationship Diagram

```
┌─────────────┐
│  CATEGORY   │
│             │
│ - id        │
│ - name      │
│ - color     │
└──────┬──────┘
       │
       │ has many
       │
       ▼
┌─────────────┐       ┌─────────────┐
│  MERCHANT   │       │   PRODUCT   │
│             │       │             │
│ - id        │       │ - id        │
│ - name      │       │ - name      │
│ - location  │       │ - barcode   │
│ - notes     │       │ - price     │
│ - photo     │       │ - category  │◄─────┐
└──────┬──────┘       │ - volume    │      │
       │              │ - photo     │      │
       │              └──────┬──────┘      │
       │                     │             │
       │                     │             │
       │ has many            │ appears in  │
       │                     │             │
       ▼                     ▼             │
┌─────────────┐       ┌─────────────┐     │
│   RECEIPT   │       │ RECEIPT_ITEM│     │
│             │       │             │     │
│ - id        │◄──────│ - receipt_id│     │
│ - code      │       │ - product_id│─────┘
│ - merchant  │       │ - quantity  │
│ - date      │       │ - price     │
│ - total     │       │ - is_labeled│
│ - photo     │       └─────────────┘
└─────────────┘
```

### 1. Category Model

**Purpose**: Organize products into logical groups

```json
{
  "id": 1,
  "name": "Dairy",
  "color": "#3B82F6",
  "description": "Milk, cheese, yogurt products",
  "product_count": 45
}
```

**Required Fields**: `name`, `color`  
**Optional Fields**: `description`  
**Calculated Fields**: `product_count` (count of products in category)

---

### 2. Merchant Model

**Purpose**: Store information about retail locations

```json
{
  "id": 4001,
  "name": "Continente",
  "location": "Faro Centro",
  "notes": "Main supermarket near city center. Open daily 8:00-22:00.",
  "photo_url": "/uploads/merchants/4001.jpg",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-11-10T14:32:00Z",
  "total_receipts": 8,
  "last_visit": "2025-11-10"
}
```

**Required Fields**: `name`, `location`  
**Optional Fields**: `notes`, `photo_url`  
**Calculated Fields**: `total_receipts`, `last_visit`

**Business Rules**:
- Merchant must exist before creating receipts
- Location should be specific (e.g., "Faro Centro" not just "Faro")
- Notes are optional but recommended for operating hours, parking info, etc.

---

### 3. Product Model

**Purpose**: Track individual products with pricing and categorization

```json
{
  "id": 2001,
  "name": "Leite Mimosa Magro 1L",
  "barcode": "5600308532147",
  "category_id": 1,
  "category_name": "Dairy",
  "price": 0.89,
  "volume": "L",
  "volume_amount": 1.0,
  "description": "Fresh semi-skimmed milk, 1.5% fat content.",
  "photo_url": "/uploads/products/2001.jpg",
  "created_at": "2025-01-20T09:15:00Z",
  "updated_at": "2025-11-05T11:20:00Z",
  "last_price_change": "2025-10-15T00:00:00Z",
  "price_history": [
    {"date": "2025-01-20", "price": 0.85},
    {"date": "2025-06-10", "price": 0.87},
    {"date": "2025-10-15", "price": 0.89}
  ]
}
```

**Required Fields**: `name`, `category_id`, `price`, `volume`  
**Optional Fields**: `barcode`, `description`, `photo_url`, `volume_amount`  
**Calculated Fields**: `category_name`, `last_price_change`, `price_history`

**Volume Types**: `kg`, `g`, `L`, `mL`, `u` (units)

**Business Rules**:
- Product must have a category
- Price must be greater than 0
- Barcode should be unique if provided
- Price history tracks all changes for analytics

---

### 4. Receipt Model

**Purpose**: Record purchase transactions

```json
{
  "id": 1001,
  "code": "RCPT-2025-1001-CON",
  "merchant_id": 4001,
  "merchant_name": "Continente",
  "date": "2025-11-10",
  "time": "14:32:00",
  "total": 11.70,
  "photo_url": "/uploads/receipts/1001.jpg",
  "notes": "Weekly grocery shopping",
  "created_at": "2025-11-10T14:45:00Z",
  "updated_at": "2025-11-10T14:45:00Z",
  "item_count": 3,
  "items": [
    {
      "id": 1,
      "product_id": 2001,
      "product_name": "Leite Mimosa Magro 1L",
      "quantity": 2,
      "price": 2.38,
      "unit_price": 1.19,
      "is_labeled": true
    },
    {
      "id": 2,
      "product_id": 2002,
      "product_name": "Pão de Forma Integral",
      "quantity": 1,
      "price": 1.85,
      "unit_price": 1.85,
      "is_labeled": false
    },
    {
      "id": 3,
      "product_id": 2003,
      "product_name": "Maçãs Golden 1kg",
      "quantity": 3,
      "price": 7.47,
      "unit_price": 2.49,
      "is_labeled": true
    }
  ]
}
```

**Required Fields**: `merchant_id`, `date`, `items[]`  
**Optional Fields**: `code`, `time`, `photo_url`, `notes`  
**Calculated Fields**: `total` (sum of all items), `item_count`, `merchant_name`

**Receipt Item Fields**:
- `product_id`: Link to product
- `quantity`: Number of units purchased
- `price`: Total price for this line item (quantity × unit_price)
- `unit_price`: Price per unit at time of purchase
- `is_labeled`: Product marked as white label/own brand

**Business Rules**:
- Receipt must have at least 1 item
- Total is automatically calculated: `SUM(items.price)`
- Each item stores the price at time of purchase (historical pricing)
- Merchant must exist before creating receipt

---

## API Endpoints Reference

All endpoints should follow RESTful conventions. Here's the expected API structure:

### Base URL
```
http://your-api-domain.com/api
```

### Authentication
If your API requires authentication, include the token in headers:
```javascript
headers: {
    'Authorization': 'Bearer YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}
```

---

### Category Endpoints

#### List All Categories
```http
GET /api/categories
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Dairy",
      "color": "#3B82F6",
      "product_count": 45
    },
    {
      "id": 2,
      "name": "Bakery",
      "color": "#F59E0B",
      "product_count": 32
    }
  ],
  "total": 10
}
```

#### Get Single Category
```http
GET /api/categories/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Dairy",
    "color": "#3B82F6",
    "description": "Milk, cheese, yogurt products",
    "product_count": 45,
    "products": [
      {
        "id": 2001,
        "name": "Leite Mimosa Magro 1L",
        "price": 0.89
      }
    ]
  }
}
```

#### Create Category
```http
POST /api/categories
Content-Type: application/json

{
  "name": "Frozen",
  "color": "#8B5CF6",
  "description": "Frozen food products"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 11,
    "name": "Frozen",
    "color": "#8B5CF6",
    "description": "Frozen food products",
    "product_count": 0
  },
  "message": "Category created successfully"
}
```

#### Update Category
```http
PUT /api/categories/{id}
Content-Type: application/json

{
  "name": "Frozen Foods",
  "color": "#8B5CF6",
  "description": "All frozen food products"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 11,
    "name": "Frozen Foods",
    "color": "#8B5CF6",
    "description": "All frozen food products",
    "product_count": 0
  },
  "message": "Category updated successfully"
}
```

#### Delete Category
```http
DELETE /api/categories/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Category deleted successfully"
}
```

**Error** (400 Bad Request) - if category has products:
```json
{
  "success": false,
  "error": "Cannot delete category with existing products",
  "product_count": 12
}
```

---

### Merchant Endpoints

#### List All Merchants
```http
GET /api/merchants
```

**Query Parameters**:
- `sort`: `name`, `last_visit`, `total_receipts` (default: `name`)
- `order`: `asc`, `desc` (default: `asc`)

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 4001,
      "name": "Continente",
      "location": "Faro Centro",
      "total_receipts": 8,
      "last_visit": "2025-11-10",
      "photo_url": "/uploads/merchants/4001.jpg"
    }
  ],
  "total": 5
}
```

#### Get Single Merchant
```http
GET /api/merchants/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 4001,
    "name": "Continente",
    "location": "Faro Centro",
    "notes": "Main supermarket near city center.",
    "photo_url": "/uploads/merchants/4001.jpg",
    "total_receipts": 8,
    "last_visit": "2025-11-10",
    "recent_receipts": [
      {
        "id": 1001,
        "code": "RCPT-2025-1001-CON",
        "date": "2025-11-10",
        "total": 11.70,
        "item_count": 3
      }
    ]
  }
}
```

#### Create Merchant
```http
POST /api/merchants
Content-Type: application/json

{
  "name": "Pingo Doce",
  "location": "Faro Shopping",
  "notes": "Inside shopping mall, parking available"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 4002,
    "name": "Pingo Doce",
    "location": "Faro Shopping",
    "notes": "Inside shopping mall, parking available",
    "photo_url": null,
    "total_receipts": 0,
    "last_visit": null
  },
  "message": "Merchant created successfully"
}
```

#### Update Merchant
```http
PUT /api/merchants/{id}
Content-Type: application/json

{
  "name": "Continente Bom Dia",
  "location": "Faro Centro",
  "notes": "Updated operating hours: 7:00-23:00"
}
```

#### Upload Merchant Photo
```http
POST /api/merchants/{id}/photo
Content-Type: multipart/form-data

photo: [binary file data]
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "photo_url": "/uploads/merchants/4001.jpg"
  },
  "message": "Photo uploaded successfully"
}
```

#### Delete Merchant
```http
DELETE /api/merchants/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Merchant deleted successfully"
}
```

**Error** (400 Bad Request) - if merchant has receipts:
```json
{
  "success": false,
  "error": "Cannot delete merchant with existing receipts",
  "receipt_count": 8
}
```

---

### Product Endpoints

#### List All Products
```http
GET /api/products
```

**Query Parameters**:
- `category`: Filter by category ID
- `search`: Search by name or barcode
- `sort`: `name`, `price`, `updated_at` (default: `name`)
- `order`: `asc`, `desc` (default: `asc`)

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 2001,
      "name": "Leite Mimosa Magro 1L",
      "barcode": "5600308532147",
      "category_id": 1,
      "category_name": "Dairy",
      "price": 0.89,
      "volume": "L",
      "photo_url": "/uploads/products/2001.jpg"
    }
  ],
  "total": 150
}
```

#### Get Single Product
```http
GET /api/products/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 2001,
    "name": "Leite Mimosa Magro 1L",
    "barcode": "5600308532147",
    "category_id": 1,
    "category_name": "Dairy",
    "price": 0.89,
    "volume": "L",
    "volume_amount": 1.0,
    "description": "Fresh semi-skimmed milk, 1.5% fat content.",
    "photo_url": "/uploads/products/2001.jpg",
    "price_history": [
      {"date": "2025-01-20", "price": 0.85},
      {"date": "2025-10-15", "price": 0.89}
    ]
  }
}
```

#### Create Product
```http
POST /api/products
Content-Type: application/json

{
  "name": "Iogurte Natural",
  "barcode": "5601234567890",
  "category_id": 1,
  "price": 0.45,
  "volume": "u",
  "volume_amount": 1,
  "description": "Natural yogurt, no added sugar"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 2150,
    "name": "Iogurte Natural",
    "barcode": "5601234567890",
    "category_id": 1,
    "price": 0.45,
    "volume": "u"
  },
  "message": "Product created successfully"
}
```

#### Update Product
```http
PUT /api/products/{id}
Content-Type: application/json

{
  "name": "Iogurte Natural Grego",
  "price": 0.55,
  "description": "Greek style natural yogurt"
}
```

**Note**: When price changes, the system should:
1. Update the current price
2. Add entry to price_history
3. Update `last_price_change` timestamp

#### Upload Product Photo
```http
POST /api/products/{id}/photo
Content-Type: multipart/form-data

photo: [binary file data]
```

#### Delete Product
```http
DELETE /api/products/{id}
```

---

### Receipt Endpoints

#### List All Receipts
```http
GET /api/receipts
```

**Query Parameters**:
- `merchant_id`: Filter by merchant
- `date_from`: Filter by date range (YYYY-MM-DD)
- `date_to`: Filter by date range (YYYY-MM-DD)
- `sort`: `date`, `total`, `merchant` (default: `date`)
- `order`: `asc`, `desc` (default: `desc`)

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1001,
      "code": "RCPT-2025-1001-CON",
      "merchant_id": 4001,
      "merchant_name": "Continente",
      "date": "2025-11-10",
      "time": "14:32:00",
      "total": 11.70,
      "item_count": 3,
      "photo_url": "/uploads/receipts/1001.jpg"
    }
  ],
  "total": 45
}
```

#### Get Single Receipt
```http
GET /api/receipts/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1001,
    "code": "RCPT-2025-1001-CON",
    "merchant_id": 4001,
    "merchant_name": "Continente",
    "merchant_location": "Faro Centro",
    "date": "2025-11-10",
    "time": "14:32:00",
    "total": 11.70,
    "photo_url": "/uploads/receipts/1001.jpg",
    "notes": "Weekly grocery shopping",
    "item_count": 3,
    "items": [
      {
        "id": 1,
        "product_id": 2001,
        "product_name": "Leite Mimosa Magro 1L",
        "category_name": "Dairy",
        "barcode": "5600308532147",
        "quantity": 2,
        "price": 2.38,
        "unit_price": 1.19,
        "is_labeled": true
      },
      {
        "id": 2,
        "product_id": 2002,
        "product_name": "Pão de Forma Integral",
        "category_name": "Bakery",
        "barcode": "5600123456789",
        "quantity": 1,
        "price": 1.85,
        "unit_price": 1.85,
        "is_labeled": false
      }
    ]
  }
}
```

#### Create Receipt
```http
POST /api/receipts
Content-Type: application/json

{
  "merchant_id": 4001,
  "date": "2025-11-14",
  "time": "15:30:00",
  "notes": "Weekly shopping",
  "items": [
    {
      "product_id": 2001,
      "quantity": 2,
      "unit_price": 1.19,
      "is_labeled": true
    },
    {
      "product_id": 2002,
      "quantity": 1,
      "unit_price": 1.85,
      "is_labeled": false
    }
  ]
}
```

**Backend Calculations**:
```javascript
// For each item:
item.price = item.quantity * item.unit_price

// For receipt:
receipt.total = items.reduce((sum, item) => sum + item.price, 0)
receipt.item_count = items.length
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 1025,
    "code": "RCPT-2025-1025-CON",
    "merchant_id": 4001,
    "date": "2025-11-14",
    "total": 4.23,
    "item_count": 2
  },
  "message": "Receipt created successfully"
}
```

#### Update Receipt
```http
PUT /api/receipts/{id}
Content-Type: application/json

{
  "date": "2025-11-14",
  "time": "16:00:00",
  "notes": "Updated notes",
  "items": [
    {
      "id": 1,
      "product_id": 2001,
      "quantity": 3,
      "unit_price": 1.19,
      "is_labeled": true
    }
  ]
}
```

**Note**: When updating items:
- Include `id` for existing items to update them
- Omit `id` for new items to create them
- Items not included in the array will be deleted

#### Upload Receipt Photo
```http
POST /api/receipts/{id}/photo
Content-Type: multipart/form-data

photo: [binary file data]
```

#### Delete Receipt
```http
DELETE /api/receipts/{id}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Receipt deleted successfully"
}
```

---

### Error Handling

All endpoints should return consistent error responses:

**400 Bad Request** - Validation error:
```json
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "name": "Name is required",
    "price": "Price must be greater than 0"
  }
}
```

**404 Not Found**:
```json
{
  "success": false,
  "error": "Resource not found",
  "resource": "product",
  "id": 9999
}
```

**500 Internal Server Error**:
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Frontend Integration

### Setting Up API Communication

Create a utility module for API calls: `js/api.js`

```javascript
// js/api.js
class API {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // GET request
    async get(endpoint) {
        return this.request(endpoint, {
            method: 'GET'
        });
    }

    // POST request
    async post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    }

    // PUT request
    async put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body)
        });
    }

    // DELETE request
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }

    // Upload file (multipart/form-data)
    async uploadFile(endpoint, file, fieldName = 'photo') {
        const formData = new FormData();
        formData.append(fieldName, file);

        return this.request(endpoint, {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set Content-Type for multipart
        });
    }
}

// Initialize API instance
const api = new API(API_CONFIG.baseURL);
```

### Using the API Module

Include in your HTML pages:
```html
<script src="../js/config.js"></script>
<script src="../js/api.js"></script>
```

---

## Complete Workflow Examples

### Workflow 1: Creating a Complete Receipt (Step-by-Step)

This is the most common workflow: Create Merchant → Create Products → Create Receipt

#### Step 1: Create Merchant

**Frontend: `merchant/add.html`**

```javascript
// merchant-add.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Collect form data
        const merchantData = {
            name: document.getElementById('merchant-name').value,
            location: document.getElementById('merchant-location').value,
            notes: document.getElementById('merchant-notes').value
        };
        
        try {
            // Create merchant
            const response = await api.post('/merchants', merchantData);
            
            if (response.success) {
                const merchantId = response.data.id;
                
                // Upload photo if selected
                const photoInput = document.getElementById('merchant-photo');
                if (photoInput.files.length > 0) {
                    await api.uploadFile(
                        `/merchants/${merchantId}/photo`,
                        photoInput.files[0]
                    );
                }
                
                // Show success message
                alert('Merchant created successfully!');
                
                // Redirect to merchant view
                window.location.href = `view-example.html?id=${merchantId}`;
            }
        } catch (error) {
            alert('Error creating merchant: ' + error.message);
        }
    });
});
```

**HTML Form Structure:**
```html
<form id="merchant-form">
    <div class="form-group">
        <label class="form-label">Merchant Name *</label>
        <input type="text" id="merchant-name" class="form-input" required>
    </div>

    <div class="photo-upload-container">
        <div class="form-group form-group-no-margin">
            <label class="form-label">Merchant Photo</label>
            <div class="file-upload photo-upload-small">
                <input type="file" id="merchant-photo" class="file-upload-input" accept="image/*">
                <label for="merchant-photo" class="file-upload-label photo-upload-label-content">
                    <div class="photo-upload-icon">📷</div>
                    <div class="photo-upload-text">Upload Photo</div>
                </label>
            </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            <div class="form-group form-group-no-margin">
                <label class="form-label">Location *</label>
                <input type="text" id="merchant-location" class="form-input" required>
            </div>

            <div class="form-group form-group-no-margin">
                <label class="form-label">Notes</label>
                <textarea id="merchant-notes" class="form-textarea resize-vertical"></textarea>
            </div>
        </div>
    </div>

    <div class="flex flex-gap justify-end mt-2">
        <a href="list.html" class="btn btn-outline">Cancel</a>
        <button type="submit" class="btn btn-success">Add Merchant</button>
    </div>
</form>
```

---

#### Step 2: Create Products

**Frontend: `product/add.html`**

```javascript
// product-add.js
document.addEventListener('DOMContentLoaded', async function() {
    // Load categories for dropdown
    await loadCategories();
    
    const form = document.querySelector('form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const productData = {
            name: document.getElementById('product-name').value,
            barcode: document.getElementById('product-barcode').value || null,
            category_id: parseInt(document.getElementById('product-category').value),
            price: parseFloat(document.getElementById('product-price').value),
            volume: document.getElementById('product-volume').value,
            volume_amount: parseFloat(document.getElementById('product-volume-amount').value),
            description: document.getElementById('product-description').value || null
        };
        
        try {
            const response = await api.post('/products', productData);
            
            if (response.success) {
                const productId = response.data.id;
                
                // Upload photo if selected
                const photoInput = document.getElementById('product-photo');
                if (photoInput.files.length > 0) {
                    await api.uploadFile(
                        `/products/${productId}/photo`,
                        photoInput.files[0]
                    );
                }
                
                alert('Product created successfully!');
                window.location.href = `view-example.html?id=${productId}`;
            }
        } catch (error) {
            alert('Error creating product: ' + error.message);
        }
    });
});

async function loadCategories() {
    try {
        const response = await api.get('/categories');
        const select = document.getElementById('product-category');
        
        response.data.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}
```

---

#### Step 3: Create Receipt with Products

**Frontend: `receipt/edit-example.html`**

This is the most complex operation as it involves managing multiple products.

```javascript
// receipt-edit.js (enhanced with API integration)

let receiptData = {
    merchant_id: null,
    date: null,
    time: null,
    notes: null,
    items: []
};

// Load initial data
document.addEventListener('DOMContentLoaded', async function() {
    await loadMerchants();
    await loadProducts();
    
    const urlParams = new URLSearchParams(window.location.search);
    const receiptId = urlParams.get('id');
    
    if (receiptId) {
        // Edit mode - load existing receipt
        await loadReceipt(receiptId);
    } else {
        // Add mode - initialize empty
        initializeNewReceipt();
    }
    
    setupEventListeners();
});

async function loadMerchants() {
    try {
        const response = await api.get('/merchants');
        const select = document.getElementById('receipt-merchant');
        
        response.data.forEach(merchant => {
            const option = document.createElement('option');
            option.value = merchant.id;
            option.textContent = `${merchant.name} - ${merchant.location}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading merchants:', error);
    }
}

async function loadProducts() {
    try {
        const response = await api.get('/products');
        // Store products for autocomplete/search
        window.availableProducts = response.data;
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function loadReceipt(receiptId) {
    try {
        const response = await api.get(`/receipts/${receiptId}`);
        const receipt = response.data;
        
        // Populate form fields
        document.getElementById('receipt-code').value = receipt.code || '';
        document.getElementById('receipt-merchant').value = receipt.merchant_id;
        document.getElementById('receipt-date').value = receipt.date;
        document.getElementById('receipt-time').value = receipt.time || '';
        document.getElementById('receipt-notes').value = receipt.notes || '';
        
        // Load products list
        const productsList = document.getElementById('products-list');
        productsList.innerHTML = '';
        
        receipt.items.forEach(item => {
            addProductRow(item);
        });
        
        updateProductCount();
    } catch (error) {
        console.error('Error loading receipt:', error);
        alert('Error loading receipt');
    }
}

function initializeNewReceipt() {
    // Set today's date by default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('receipt-date').value = today;
    
    // Set current time
    const now = new Date();
    const time = now.toTimeString().split(' ')[0].substring(0, 5);
    document.getElementById('receipt-time').value = time;
}

function setupEventListeners() {
    // Add product button
    const addBtn = document.querySelector('[data-action="add-product"]');
    addBtn.addEventListener('click', () => addProductRow());
    
    // Remove product buttons (event delegation)
    const productsList = document.getElementById('products-list');
    productsList.addEventListener('click', function(e) {
        const removeBtn = e.target.closest('[data-action="remove-product"]');
        if (removeBtn) {
            removeProduct(removeBtn);
        }
    });
    
    // Form submit
    const form = document.querySelector('form');
    form.addEventListener('submit', handleSubmit);
}

function addProductRow(itemData = null) {
    const productsList = document.getElementById('products-list');
    
    const row = document.createElement('div');
    row.className = 'list-item receipt-products-edit-grid';
    row.innerHTML = `
        <input type="text" 
               class="form-input-compact product-name-input" 
               value="${itemData?.product_name || ''}" 
               placeholder="Product name"
               data-product-id="${itemData?.product_id || ''}"
               list="products-datalist">
        <input type="number" 
               class="form-input-compact form-input-number-xs" 
               value="${itemData?.quantity || 1}" 
               min="1">
        <input type="number" 
               class="form-input-compact form-input-number-sm" 
               value="${itemData?.unit_price || '0.00'}" 
               step="0.01" 
               min="0">
        <input type="checkbox" 
               class="checkbox-large" 
               ${itemData?.is_labeled ? 'checked' : ''}>
        <button class="btn btn-sm btn-danger btn-icon-sm" 
                data-action="remove-product">−</button>
    `;
    
    productsList.appendChild(row);
    updateProductCount();
    
    // Focus on product name input
    const nameInput = row.querySelector('.product-name-input');
    nameInput.focus();
    
    // Add autocomplete functionality
    setupProductAutocomplete(nameInput);
}

function setupProductAutocomplete(input) {
    // Create datalist if not exists
    let datalist = document.getElementById('products-datalist');
    if (!datalist) {
        datalist = document.createElement('datalist');
        datalist.id = 'products-datalist';
        document.body.appendChild(datalist);
        
        // Populate with products
        window.availableProducts.forEach(product => {
            const option = document.createElement('option');
            option.value = product.name;
            option.dataset.productId = product.id;
            option.dataset.price = product.price;
            datalist.appendChild(option);
        });
    }
    
    // Auto-fill price when product is selected
    input.addEventListener('change', function() {
        const selectedProduct = window.availableProducts.find(
            p => p.name === this.value
        );
        
        if (selectedProduct) {
            this.dataset.productId = selectedProduct.id;
            const priceInput = this.parentElement.querySelector('.form-input-number-sm');
            priceInput.value = selectedProduct.price.toFixed(2);
        }
    });
}

function removeProduct(button) {
    const row = button.closest('.list-item');
    row.remove();
    updateProductCount();
}

function updateProductCount() {
    const productsList = document.getElementById('products-list');
    const productsTitle = document.getElementById('products-title');
    const count = productsList.querySelectorAll('.list-item').length;
    productsTitle.textContent = `Products in Receipt (${count})`;
}

async function handleSubmit(e) {
    e.preventDefault();
    
    // Collect receipt data
    const receiptData = {
        merchant_id: parseInt(document.getElementById('receipt-merchant').value),
        date: document.getElementById('receipt-date').value,
        time: document.getElementById('receipt-time').value || null,
        notes: document.getElementById('receipt-notes').value || null,
        items: []
    };
    
    // Collect all products
    const productRows = document.querySelectorAll('.receipt-products-edit-grid.list-item');
    productRows.forEach(row => {
        const nameInput = row.querySelector('.product-name-input');
        const quantityInput = row.querySelector('.form-input-number-xs');
        const priceInput = row.querySelector('.form-input-number-sm');
        const labelCheckbox = row.querySelector('.checkbox-large');
        
        const productId = parseInt(nameInput.dataset.productId);
        if (!productId) {
            alert('Please select valid products from the list');
            throw new Error('Invalid product');
        }
        
        receiptData.items.push({
            product_id: productId,
            quantity: parseInt(quantityInput.value),
            unit_price: parseFloat(priceInput.value),
            is_labeled: labelCheckbox.checked
        });
    });
    
    // Validate
    if (receiptData.items.length === 0) {
        alert('Please add at least one product');
        return;
    }
    
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const receiptId = urlParams.get('id');
        
        let response;
        if (receiptId) {
            // Update existing receipt
            response = await api.put(`/receipts/${receiptId}`, receiptData);
        } else {
            // Create new receipt
            response = await api.post('/receipts', receiptData);
        }
        
        if (response.success) {
            // Upload photo if selected
            const photoInput = document.getElementById('receipt-photo');
            if (photoInput && photoInput.files.length > 0) {
                const id = receiptId || response.data.id;
                await api.uploadFile(`/receipts/${id}/photo`, photoInput.files[0]);
            }
            
            alert('Receipt saved successfully!');
            window.location.href = `view-example.html?id=${response.data.id}`;
        }
    } catch (error) {
        alert('Error saving receipt: ' + error.message);
    }
}
```

**Key Features in Receipt Edit**:
1. ✅ Loads merchants and products from API
2. ✅ Product autocomplete with datalist
3. ✅ Auto-fills price when product selected
4. ✅ Validates product selection
5. ✅ Handles both create and update operations
6. ✅ Uploads photo after receipt creation
7. ✅ Dynamic product row management

---

### Workflow 2: Viewing Data (List & Detail Pages)

#### Loading List Page

**Frontend: `merchant/list.html`**

```javascript
// merchant-list.js
document.addEventListener('DOMContentLoaded', async function() {
    await loadMerchants();
});

async function loadMerchants() {
    try {
        const response = await api.get('/merchants?sort=name&order=asc');
        const tableBody = document.getElementById('merchants-table-body');
        tableBody.innerHTML = '';
        
        if (response.data.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center" style="padding: 2rem;">
                        No merchants found. <a href="add.html">Add your first merchant</a>
                    </td>
                </tr>
            `;
            return;
        }
        
        response.data.forEach(merchant => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <a href="view-example.html?id=${merchant.id}" class="link-primary">
                        ${merchant.name}
                    </a>
                </td>
                <td>${merchant.location}</td>
                <td class="text-center">${merchant.total_receipts}</td>
                <td class="text-center">
                    ${merchant.last_visit ? formatDate(merchant.last_visit) : 'Never'}
                </td>
            `;
            tableBody.appendChild(row);
        });
        
        // Update total count
        document.getElementById('total-count').textContent = response.data.length;
    } catch (error) {
        console.error('Error loading merchants:', error);
        alert('Error loading merchants');
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB'); // DD/MM/YYYY format
}
```

**HTML Table Structure:**
```html
<div class="card">
    <div class="flex flex-between mb-1-5">
        <h2 class="section-title">
            All Merchants (<span id="total-count">0</span>)
        </h2>
        <a href="add.html" class="btn btn-primary">Add Merchant</a>
    </div>
    
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Location</th>
                <th class="text-center">Receipts</th>
                <th class="text-center">Last Visit</th>
            </tr>
        </thead>
        <tbody id="merchants-table-body">
            <!-- Populated by JavaScript -->
        </tbody>
    </table>
</div>

<script src="../js/config.js"></script>
<script src="../js/api.js"></script>
<script src="../js/merchant-list.js"></script>
```

---

#### Loading Detail Page

**Frontend: `product/view-example.html`**

```javascript
// product-view.js
document.addEventListener('DOMContentLoaded', async function() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (!productId) {
        alert('Product ID not specified');
        window.location.href = 'list.html';
        return;
    }
    
    await loadProduct(productId);
    await renderPriceChart(productId);
});

async function loadProduct(productId) {
    try {
        const response = await api.get(`/products/${productId}`);
        const product = response.data;
        
        // Update page title
        document.querySelector('.page-title').textContent = product.name;
        
        // Update photo
        const photoImg = document.getElementById('product-image');
        const photoPlaceholder = document.getElementById('no-photo-placeholder');
        
        if (product.photo_url) {
            photoImg.src = product.photo_url;
            photoImg.style.display = 'block';
            photoPlaceholder.style.display = 'none';
        }
        
        // Update product info
        document.querySelector('[data-field="category"]').textContent = product.category_name;
        document.querySelector('[data-field="volume"]').textContent = 
            `${product.volume_amount} ${product.volume}`;
        document.querySelector('[data-field="barcode"]').textContent = 
            product.barcode || 'N/A';
        document.querySelector('[data-field="price"]').textContent = 
            `${product.price.toFixed(2)} € / ${product.volume}`;
        
        // Update description if exists
        if (product.description) {
            document.querySelector('[data-field="description"]').textContent = 
                product.description;
        }
        
        // Store price history for chart
        window.productPriceHistory = product.price_history || [];
        
    } catch (error) {
        console.error('Error loading product:', error);
        alert('Error loading product');
        window.location.href = 'list.html';
    }
}

async function renderPriceChart(productId) {
    const history = window.productPriceHistory;
    
    if (history.length === 0) {
        document.getElementById('priceHistoryChart').style.display = 'none';
        return;
    }
    
    const ctx = document.getElementById('priceHistoryChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: history.map(h => formatDate(h.date)),
            datasets: [{
                label: 'Price (€)',
                data: history.map(h => h.price),
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2) + ' €';
                        }
                    }
                }
            }
        }
    });
}
```

**HTML Structure with Data Attributes:**
```html
<div class="product-info-grid">
    <div class="product-info-item">
        <span class="product-info-label">Category</span>
        <span class="product-info-value" data-field="category">Loading...</span>
    </div>
    <div class="product-info-item">
        <span class="product-info-label">Volume</span>
        <span class="product-info-value" data-field="volume">Loading...</span>
    </div>
    <div class="product-info-item">
        <span class="product-info-label">Barcode</span>
        <span class="product-info-value" data-field="barcode">Loading...</span>
    </div>
    <div class="product-price-section">
        <span class="product-info-label">Current Price</span>
        <span class="product-price-value" data-field="price">Loading...</span>
    </div>
</div>
```

---

## HTML Structure Guide

Understanding the HTML component patterns is crucial for maintaining consistency across pages.

### Page Template Structure

Every page follows this basic structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title - InfinExpense</title>
    <link rel="stylesheet" href="../css/main.css">
</head>
<body data-active-page="entity-name">
    <!-- Navigation Template (loaded dynamically) -->
    <div data-template="header"></div>
    <script src="../js/template-loader.js"></script>

    <!-- Main Content -->
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Page Title</h1>
            <div class="flex flex-gap">
                <!-- Action buttons -->
            </div>
        </div>

        <!-- Page-specific content here -->
    </div>

    <!-- Scripts -->
    <script src="../js/config.js"></script>
    <script src="../js/api.js"></script>
    <script src="../js/page-specific.js"></script>
</body>
</html>
```

**Key Elements**:
- `data-active-page`: Highlights active menu item (values: `merchants`, `products`, `receipts`, `categories`)
- `data-template="header"`: Navigation loads here automatically
- `.container`: Main content wrapper with proper padding/max-width
- `.page-header`: Consistent header layout with title and actions

---

### List Page Pattern

Used for: `merchant/list.html`, `product/list.html`, `receipt/list.html`, `category/list.html`

```html
<div class="container">
    <div class="page-header">
        <h1 class="page-title">All Merchants (<span id="total-count">0</span>)</h1>
        <div class="flex flex-gap">
            <a href="add.html" class="btn btn-primary">Add Merchant</a>
        </div>
    </div>

    <!-- Search/Filter Section (Optional) -->
    <div class="card mb-1-5">
        <div class="form-row">
            <div class="form-group">
                <label class="form-label">Search</label>
                <input type="text" id="search-input" class="form-input" placeholder="Search by name...">
            </div>
            <div class="form-group">
                <label class="form-label">Sort By</label>
                <select id="sort-select" class="form-select">
                    <option value="name">Name</option>
                    <option value="date">Date</option>
                    <option value="total">Total</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Table View -->
    <div class="card">
        <table class="table">
            <thead>
                <tr>
                    <th>Column 1</th>
                    <th>Column 2</th>
                    <th class="text-center">Column 3</th>
                    <th class="text-right">Actions</th>
                </tr>
            </thead>
            <tbody id="data-table-body">
                <!-- Populated by JavaScript -->
            </tbody>
        </table>
    </div>
</div>
```

**JavaScript Pattern for Lists**:
```javascript
async function loadData() {
    const response = await api.get('/endpoint');
    const tbody = document.getElementById('data-table-body');
    tbody.innerHTML = '';
    
    response.data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <a href="view-example.html?id=${item.id}" class="link-primary">
                    ${item.name}
                </a>
            </td>
            <td>${item.field2}</td>
            <td class="text-center">${item.field3}</td>
            <td class="text-right">
                <a href="edit-example.html?id=${item.id}" class="btn btn-sm btn-outline">Edit</a>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    document.getElementById('total-count').textContent = response.data.length;
}
```

---

### View/Detail Page Pattern

Used for: `merchant/view-example.html`, `product/view-example.html`, `receipt/view-example.html`

```html
<div class="container">
    <div class="page-header">
        <h1 class="page-title" id="entity-name">Loading...</h1>
        <div class="flex flex-gap">
            <a href="edit-example.html?id=ID" class="btn btn-primary" id="edit-btn">Edit</a>
            <button class="btn btn-danger" id="delete-btn">Delete</button>
        </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid-2cols-1-2">
        <!-- LEFT COLUMN: Main Info -->
        <div class="card product-detail-layout">
            <!-- Photo Section -->
            <div class="product-photo-container">
                <img id="entity-image" 
                     src="" 
                     alt="Entity Photo" 
                     class="image-preview"
                     style="display: none; cursor: pointer;">
                <div id="no-photo-placeholder" class="no-photo-placeholder">
                    <div class="no-photo-icon">🚫</div>
                    <div class="no-photo-text">NO PHOTO</div>
                </div>
            </div>

            <!-- Info Grid -->
            <div class="product-info-grid">
                <div class="product-info-item">
                    <span class="product-info-label">Field 1</span>
                    <span class="product-info-value" data-field="field1">-</span>
                </div>
                <div class="product-info-item">
                    <span class="product-info-label">Field 2</span>
                    <span class="product-info-value" data-field="field2">-</span>
                </div>
                <div class="product-price-section">
                    <span class="product-info-label">Price/Total</span>
                    <span class="product-price-value" data-field="price">0.00 €</span>
                </div>
            </div>
        </div>

        <!-- RIGHT COLUMN: Related Data or Charts -->
        <div class="card">
            <h3 class="detail-title">Related Items</h3>
            
            <!-- List View -->
            <div class="scrollable-list">
                <div class="list-container" id="related-items">
                    <!-- Populated by JavaScript -->
                </div>
            </div>
        </div>
    </div>
</div>
```

**Photo Display Logic**:
```javascript
function displayPhoto(photoUrl) {
    const img = document.getElementById('entity-image');
    const placeholder = document.getElementById('no-photo-placeholder');
    
    if (photoUrl) {
        img.src = photoUrl;
        img.style.display = 'block';
        placeholder.style.display = 'none';
        
        // Add click to view full size
        img.addEventListener('click', () => {
            window.open(photoUrl, '_blank');
        });
    } else {
        img.style.display = 'none';
        placeholder.style.display = 'flex';
    }
}
```

---

### Add/Edit Form Pattern

Used for: `merchant/add.html`, `product/edit-example.html`, etc.

```html
<div class="container">
    <div class="page-header">
        <h1 class="page-title">Add/Edit Entity</h1>
    </div>

    <div class="card">
        <form id="entity-form">
            <!-- Text Input -->
            <div class="form-group">
                <label class="form-label">Field Name *</label>
                <input type="text" 
                       id="field-name" 
                       class="form-input" 
                       placeholder="Enter value" 
                       required>
            </div>

            <!-- Photo Upload (if applicable) -->
            <div class="photo-upload-container">
                <div class="form-group form-group-no-margin">
                    <label class="form-label">Photo</label>
                    <div class="file-upload photo-upload-small">
                        <input type="file" 
                               id="entity-photo" 
                               class="file-upload-input" 
                               accept="image/*">
                        <label for="entity-photo" 
                               class="file-upload-label photo-upload-label-content">
                            <div class="photo-upload-icon">📷</div>
                            <div class="photo-upload-text">Upload Photo</div>
                        </label>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <!-- Other fields in right column -->
                    <div class="form-group form-group-no-margin">
                        <label class="form-label">Field 2 *</label>
                        <input type="text" id="field2" class="form-input" required>
                    </div>
                </div>
            </div>

            <!-- Select/Dropdown -->
            <div class="form-group">
                <label class="form-label">Category *</label>
                <select id="category-select" class="form-select" required>
                    <option value="">Select a category</option>
                    <!-- Options populated by JavaScript -->
                </select>
            </div>

            <!-- Form Row (Multiple fields in one row) -->
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label">Field A *</label>
                    <input type="text" id="field-a" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Field B *</label>
                    <input type="text" id="field-b" class="form-input" required>
                </div>
            </div>

            <!-- Textarea -->
            <div class="form-group">
                <label class="form-label">Notes</label>
                <textarea id="notes" 
                          class="form-textarea" 
                          placeholder="Optional notes..."></textarea>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-gap justify-end mt-2">
                <a href="list.html" class="btn btn-outline">Cancel</a>
                <button type="submit" class="btn btn-primary">Save</button>
            </div>
        </form>
    </div>
</div>
```

---

### Receipt Edit Grid Pattern (Special Case)

The receipt edit page has a unique grid structure for managing multiple products:

```html
<div class="card card-flex-column">
    <div class="flex flex-between mb-1">
        <h2 class="section-title" id="products-title">Products in Receipt (0)</h2>
        <button class="btn btn-sm btn-primary btn-add-icon" 
                data-action="add-product">+</button>
    </div>

    <!-- List Header -->
    <div class="list-header receipt-products-edit-grid">
        <div class="list-header-item">
            <span>Product</span>
        </div>
        <div class="list-header-item">
            <span>Quantity</span>
        </div>
        <div class="list-header-item">
            <span>Price</span>
        </div>
        <div class="list-header-item">
            <span>🏷️</span>
        </div>
        <div class="list-header-item">
            <span>Actions</span>
        </div>
    </div>

    <!-- Scrollable List -->
    <div class="scrollable-list scrollable-list-flex">
        <div class="list-container" id="products-list">
            <!-- Product rows populated here -->
            <div class="list-item receipt-products-edit-grid">
                <input type="text" 
                       class="form-input-compact" 
                       placeholder="Product name"
                       list="products-datalist">
                <input type="number" 
                       class="form-input-compact form-input-number-xs" 
                       value="1" 
                       min="1">
                <input type="number" 
                       class="form-input-compact form-input-number-sm" 
                       value="0.00" 
                       step="0.01" 
                       min="0">
                <input type="checkbox" class="checkbox-large">
                <button class="btn btn-sm btn-danger btn-icon-sm" 
                        data-action="remove-product">−</button>
            </div>
        </div>
    </div>
</div>

<!-- Datalist for product autocomplete -->
<datalist id="products-datalist">
    <!-- Options populated by JavaScript -->
</datalist>
```

**Grid Structure**:
- Column 1 (Product): `2.5fr` - Flexible, takes most space
- Column 2 (Quantity): `90px` - Fixed width for small numbers
- Column 3 (Price): `90px` - Fixed width for decimal values
- Column 4 (Label): `60px` - Checkbox only
- Column 5 (Actions): `70px` - Remove button

---

## CSS Classes Reference

Complete reference of all CSS classes used in the application.

### Layout Classes

#### Container & Spacing
```css
.container              /* Main content wrapper, max-width 1200px */
.page-header           /* Flex header with title and actions */
.page-title            /* Main page title styling */

/* Spacing Utilities */
.mb-1                  /* margin-bottom: 1rem */
.mb-1-5                /* margin-bottom: 1.5rem */
.mt-2                  /* margin-top: 2rem */
.p-1                   /* padding: 1rem */
```

#### Grid Layouts
```css
.grid-2cols-1-2        /* Two column grid: 1fr 2fr */
.form-row              /* Horizontal form fields (2 columns) */
.photo-upload-container /* Grid for photo + fields (1fr 2fr) */
```

#### Flexbox Utilities
```css
.flex                  /* display: flex */
.flex-between          /* justify-content: space-between */
.flex-gap              /* gap: 1rem */
.justify-end           /* justify-content: flex-end */
```

---

### Card & Component Classes

#### Cards
```css
.card                  /* Standard card container */
.card-flex-column      /* Card with flex column layout */
```

#### Lists
```css
.list-header           /* List header row */
.list-header-item      /* Individual header cell */
.list-item             /* Individual list item row */
.list-container        /* Container for list items */
.scrollable-list       /* Scrollable list wrapper */
.scrollable-list-flex  /* Scrollable with flex: 1 */
```

#### Special Grids
```css
.receipt-products-edit-grid    /* Receipt edit product grid */
.product-info-grid             /* Product detail info grid */
.product-detail-layout         /* Product detail page layout */
```

---

### Form Classes

#### Form Groups
```css
.form-group            /* Standard form field wrapper */
.form-group-no-margin  /* Form group without bottom margin */
.form-row              /* Horizontal form fields */
```

#### Form Inputs
```css
.form-input            /* Standard text input */
.form-input-compact    /* Smaller padding for compact forms */
.form-input-number-sm  /* Small number input (90px width) */
.form-input-number-xs  /* Extra small number input (90px width) */
.form-select           /* Select dropdown */
.form-textarea         /* Textarea field */
.form-label            /* Form field label */
```

#### File Upload
```css
.file-upload           /* File upload container */
.file-upload-input     /* Hidden file input */
.file-upload-label     /* Clickable upload label */
```

#### Photo Upload Components
```css
.photo-upload-container       /* Grid layout for photo + fields */
.photo-upload-small          /* 3:4 aspect ratio upload box */
.photo-upload-label-content  /* Upload label content wrapper */
.photo-upload-icon           /* Camera icon (2.5rem) */
.photo-upload-text           /* "Upload Photo" text */
```

---

### Button Classes

#### Base Buttons
```css
.btn                   /* Base button style */
.btn-primary           /* Primary action (blue) */
.btn-success           /* Success action (green) */
.btn-danger            /* Danger action (red) */
.btn-outline           /* Outlined button */
```

#### Button Sizes
```css
.btn-sm                /* Small button */
.btn-icon-sm           /* Icon-only small button */
.btn-add-icon          /* Add button with + icon */
```

---

### Image & Media Classes

#### Images
```css
.image-preview         /* Standard image preview */
.image-preview-standard /* Image with 3:4 aspect ratio */
```

#### No Photo Placeholder
```css
.no-photo-placeholder  /* Grey box with forbidden icon */
.no-photo-icon         /* 🚫 icon (3rem) */
.no-photo-text         /* "NO PHOTO" text */
```

---

### Table Classes

```css
.table                 /* Standard table styling */
.table th              /* Table header cells */
.table td              /* Table data cells */
```

---

### Typography & Alignment

#### Text Alignment
```css
.text-left             /* text-align: left */
.text-center           /* text-align: center */
.text-right            /* text-align: right */
```

#### Font Sizes
```css
.font-size-sm          /* Small text (0.875rem) */
.font-size-lg          /* Large text (1.125rem) */
.font-size-xl          /* Extra large text (1.5rem) */
```

#### Text Colors
```css
.text-primary-color    /* Primary brand color */
.link-primary          /* Primary link color, no underline */
```

---

### Badge & Status Classes

```css
.badge                 /* Base badge style */
.badge-primary         /* Primary color badge */
.badge-success         /* Success color badge */
.badge-warning         /* Warning color badge */
.badge-danger          /* Danger color badge */
```

---

### Special Purpose Classes

#### Checkboxes
```css
.checkbox-large        /* Large checkbox (18×18px) */
```

#### Detail Pages
```css
.detail-title          /* Section title in detail pages */
.section-title         /* Main section title */
.product-info-item     /* Info item in detail view */
.product-info-label    /* Label in info item */
.product-info-value    /* Value in info item */
.product-price-section /* Price section with emphasis */
.product-price-value   /* Large price display */
```

---

### Utility Classes

```css
.resize-vertical       /* textarea resize: vertical only */
.example-data          /* Green underlined example data */
```

---

### Usage Examples

#### Creating a Card with List
```html
<div class="card">
    <h3 class="detail-title">Recent Items</h3>
    
    <div class="scrollable-list">
        <div class="list-container">
            <div class="list-item">
                <span>Item name</span>
                <span class="badge badge-success">Active</span>
            </div>
        </div>
    </div>
</div>
```

#### Creating a Form Row
```html
<div class="form-row">
    <div class="form-group">
        <label class="form-label">First Field</label>
        <input type="text" class="form-input">
    </div>
    <div class="form-group">
        <label class="form-label">Second Field</label>
        <input type="text" class="form-input">
    </div>
</div>
```

#### Creating Action Buttons
```html
<div class="flex flex-gap justify-end mt-2">
    <a href="list.html" class="btn btn-outline">Cancel</a>
    <button type="button" class="btn btn-danger">Delete</button>
    <button type="submit" class="btn btn-primary">Save</button>
</div>
```

---

## JavaScript Integration

### Best Practices & Patterns

#### 1. Module Pattern

Organize your code into reusable modules:

```javascript
// js/modules/receipt-manager.js
const ReceiptManager = (function() {
    // Private variables
    let currentReceipt = null;
    let productsList = [];
    
    // Private methods
    function calculateTotal(items) {
        return items.reduce((sum, item) => {
            return sum + (item.quantity * item.unit_price);
        }, 0);
    }
    
    // Public API
    return {
        init: function() {
            this.loadProducts();
            this.setupEventListeners();
        },
        
        loadProducts: async function() {
            const response = await api.get('/products');
            productsList = response.data;
        },
        
        addProductRow: function(productData = null) {
            // Implementation
        },
        
        getReceiptData: function() {
            return {
                merchant_id: parseInt(document.getElementById('merchant').value),
                date: document.getElementById('date').value,
                items: this.collectItems()
            };
        },
        
        collectItems: function() {
            const rows = document.querySelectorAll('.receipt-products-edit-grid.list-item');
            const items = [];
            
            rows.forEach(row => {
                const item = {
                    product_id: parseInt(row.querySelector('.product-name-input').dataset.productId),
                    quantity: parseInt(row.querySelector('.form-input-number-xs').value),
                    unit_price: parseFloat(row.querySelector('.form-input-number-sm').value),
                    is_labeled: row.querySelector('.checkbox-large').checked
                };
                items.push(item);
            });
            
            return items;
        }
    };
})();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    ReceiptManager.init();
});
```

---

#### 2. Event Delegation

Use event delegation for dynamically added elements:

```javascript
// Good ✅ - Event delegation
document.getElementById('products-list').addEventListener('click', function(e) {
    // Remove button
    const removeBtn = e.target.closest('[data-action="remove-product"]');
    if (removeBtn) {
        removeProduct(removeBtn);
        return;
    }
    
    // Other actions...
});

// Bad ❌ - Individual listeners (will break on dynamic elements)
document.querySelectorAll('.btn-remove').forEach(btn => {
    btn.addEventListener('click', function() {
        // Won't work for dynamically added buttons
    });
});
```

---

#### 3. Data Attributes for Configuration

Use data attributes instead of inline onclick handlers:

```javascript
// Good ✅ - Data attributes
<button data-action="delete" data-id="123">Delete</button>

document.addEventListener('click', function(e) {
    const btn = e.target.closest('[data-action="delete"]');
    if (btn) {
        const id = btn.dataset.id;
        deleteItem(id);
    }
});

// Bad ❌ - Inline handlers
<button onclick="deleteItem(123)">Delete</button>
```

---

#### 4. Async/Await Error Handling

Always wrap API calls in try-catch blocks:

```javascript
async function loadData(id) {
    try {
        // Show loading state
        showLoadingSpinner();
        
        const response = await api.get(`/products/${id}`);
        
        // Hide loading state
        hideLoadingSpinner();
        
        // Process data
        displayProduct(response.data);
        
    } catch (error) {
        // Hide loading state
        hideLoadingSpinner();
        
        // Show user-friendly error
        if (error.message.includes('404')) {
            showError('Product not found');
            setTimeout(() => window.location.href = 'list.html', 2000);
        } else if (error.message.includes('network')) {
            showError('Network error. Please check your connection.');
        } else {
            showError('An error occurred. Please try again.');
        }
        
        console.error('Error loading data:', error);
    }
}
```

---

#### 5. Form Validation

Validate data before sending to API:

```javascript
function validateReceiptData(data) {
    const errors = [];
    
    // Check required fields
    if (!data.merchant_id) {
        errors.push('Please select a merchant');
    }
    
    if (!data.date) {
        errors.push('Please select a date');
    }
    
    // Validate date not in future
    const selectedDate = new Date(data.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate > today) {
        errors.push('Receipt date cannot be in the future');
    }
    
    // Check items
    if (!data.items || data.items.length === 0) {
        errors.push('Please add at least one product');
    }
    
    // Validate each item
    data.items.forEach((item, index) => {
        if (!item.product_id) {
            errors.push(`Product ${index + 1}: Invalid product selected`);
        }
        
        if (item.quantity < 1) {
            errors.push(`Product ${index + 1}: Quantity must be at least 1`);
        }
        
        if (item.unit_price <= 0) {
            errors.push(`Product ${index + 1}: Price must be greater than 0`);
        }
    });
    
    return errors;
}

// Usage
async function submitReceipt(data) {
    const errors = validateReceiptData(data);
    
    if (errors.length > 0) {
        showValidationErrors(errors);
        return;
    }
    
    // Proceed with API call
    try {
        const response = await api.post('/receipts', data);
        // Success handling
    } catch (error) {
        // Error handling
    }
}

function showValidationErrors(errors) {
    const errorHtml = errors.map(err => `<li>${err}</li>`).join('');
    alert(`Please fix the following errors:\n\n${errors.join('\n')}`);
}
```

---

#### 6. Loading States

Provide visual feedback during API calls:

```javascript
// Loading spinner utility
const LoadingSpinner = {
    element: null,
    
    init: function() {
        // Create spinner element
        this.element = document.createElement('div');
        this.element.id = 'loading-spinner';
        this.element.className = 'loading-spinner';
        this.element.innerHTML = `
            <div class="spinner"></div>
            <p>Loading...</p>
        `;
        this.element.style.display = 'none';
        document.body.appendChild(this.element);
    },
    
    show: function() {
        if (this.element) {
            this.element.style.display = 'flex';
        }
    },
    
    hide: function() {
        if (this.element) {
            this.element.style.display = 'none';
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    LoadingSpinner.init();
});

// CSS for spinner (add to your stylesheet)
/*
.loading-spinner {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3B82F6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
*/
```

---

### Error Handling & Validation

#### Client-Side Validation Rules

**Merchant Validation**:
```javascript
function validateMerchant(data) {
    const errors = [];
    
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Merchant name must be at least 2 characters');
    }
    
    if (!data.location || data.location.trim().length < 2) {
        errors.push('Location must be at least 2 characters');
    }
    
    if (data.notes && data.notes.length > 500) {
        errors.push('Notes cannot exceed 500 characters');
    }
    
    return errors;
}
```

**Product Validation**:
```javascript
function validateProduct(data) {
    const errors = [];
    
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Product name must be at least 2 characters');
    }
    
    if (!data.category_id) {
        errors.push('Please select a category');
    }
    
    if (!data.price || data.price <= 0) {
        errors.push('Price must be greater than 0');
    }
    
    if (data.price > 10000) {
        errors.push('Price seems unusually high. Please verify.');
    }
    
    if (!data.volume) {
        errors.push('Please select a volume type');
    }
    
    if (data.barcode && !/^\d{8,13}$/.test(data.barcode)) {
        errors.push('Barcode must be 8-13 digits');
    }
    
    return errors;
}
```

**Category Validation**:
```javascript
function validateCategory(data) {
    const errors = [];
    
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Category name must be at least 2 characters');
    }
    
    if (!data.color || !/^#[0-9A-F]{6}$/i.test(data.color)) {
        errors.push('Please select a valid color');
    }
    
    return errors;
}
```

---

### Photo Upload Implementation

#### Complete Photo Upload Solution

```javascript
// photo-upload.js - Reusable photo upload module
const PhotoUpload = {
    maxFileSize: 5 * 1024 * 1024, // 5MB
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg', 'image/webp'],
    
    init: function(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        
        if (!input) return;
        
        input.addEventListener('change', (e) => {
            this.handleFileSelect(e, preview);
        });
    },
    
    handleFileSelect: function(event, previewElement) {
        const file = event.target.files[0];
        
        if (!file) return;
        
        // Validate file
        const validation = this.validateFile(file);
        if (!validation.valid) {
            alert(validation.error);
            event.target.value = ''; // Clear input
            return;
        }
        
        // Show preview
        if (previewElement) {
            this.showPreview(file, previewElement);
        }
    },
    
    validateFile: function(file) {
        // Check file type
        if (!this.allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: 'Please select a valid image file (JPEG, PNG, WebP)'
            };
        }
        
        // Check file size
        if (file.size > this.maxFileSize) {
            return {
                valid: false,
                error: `File size must be less than ${this.maxFileSize / 1024 / 1024}MB`
            };
        }
        
        return { valid: true };
    },
    
    showPreview: function(file, previewElement) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Update preview image
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
            
            // Hide placeholder if exists
            const placeholder = document.getElementById('no-photo-placeholder');
            if (placeholder) {
                placeholder.style.display = 'none';
            }
        };
        
        reader.readAsDataURL(file);
    },
    
    uploadFile: async function(endpoint, file) {
        const validation = this.validateFile(file);
        if (!validation.valid) {
            throw new Error(validation.error);
        }
        
        try {
            const response = await api.uploadFile(endpoint, file);
            return response;
        } catch (error) {
            console.error('Photo upload error:', error);
            throw error;
        }
    }
};

// Usage example
document.addEventListener('DOMContentLoaded', () => {
    PhotoUpload.init('product-photo', 'product-image');
});
```

---

### Common Pitfalls & Solutions

#### Pitfall 1: Not Handling URL Parameters

**Problem**: Edit pages don't load data because ID is not extracted from URL.

**Solution**:
```javascript
// Get ID from URL
const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');

if (!id) {
    alert('ID not provided');
    window.location.href = 'list.html';
    return;
}

// Load data
loadData(id);
```

---

#### Pitfall 2: Forgetting to Parse Numbers

**Problem**: Sending string values when API expects numbers.

**Solution**:
```javascript
// Bad ❌
const data = {
    merchant_id: document.getElementById('merchant').value,  // String!
    price: document.getElementById('price').value            // String!
};

// Good ✅
const data = {
    merchant_id: parseInt(document.getElementById('merchant').value),
    price: parseFloat(document.getElementById('price').value)
};
```

---

#### Pitfall 3: Not Handling Empty Responses

**Problem**: Code crashes when API returns empty array.

**Solution**:
```javascript
async function loadData() {
    const response = await api.get('/products');
    
    // Check if data exists and is array
    if (!response.data || response.data.length === 0) {
        // Show empty state
        showEmptyState('No products found. Add your first product!');
        return;
    }
    
    // Process data
    response.data.forEach(item => displayItem(item));
}
```

---

#### Pitfall 4: Not Updating Dynamic Counts

**Problem**: Product count doesn't update when items are added/removed.

**Solution**:
```javascript
function updateProductCount() {
    const list = document.getElementById('products-list');
    const title = document.getElementById('products-title');
    const count = list.querySelectorAll('.list-item').length;
    title.textContent = `Products in Receipt (${count})`;
}

// Call after every add/remove operation
function addProduct() {
    // ... add product code ...
    updateProductCount();  // ✅ Update count
}

function removeProduct(button) {
    // ... remove product code ...
    updateProductCount();  // ✅ Update count
}
```

---

#### Pitfall 5: CORS Errors

**Problem**: API calls fail with CORS errors.

**Solution** (Backend configuration needed):
```javascript
// Backend must include CORS headers:
// Access-Control-Allow-Origin: http://your-frontend-domain.com
// Access-Control-Allow-Methods: GET, POST, PUT, DELETE
// Access-Control-Allow-Headers: Content-Type, Authorization

// For development, you might need:
// Access-Control-Allow-Origin: *

// If using Express.js:
const cors = require('cors');
app.use(cors({
    origin: 'http://localhost:3000',  // Your frontend URL
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

### Troubleshooting Guide

#### Issue: "Cannot read property of undefined"

**Cause**: Element doesn't exist in DOM when JavaScript runs.

**Solution**:
```javascript
// Wrap code in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Now safe to access DOM elements
    const element = document.getElementById('my-element');
    if (element) {
        // Use element
    }
});
```

---

#### Issue: Photo upload fails silently

**Diagnostics**:
```javascript
async function debugPhotoUpload(file) {
    console.log('File details:', {
        name: file.name,
        size: file.size,
        type: file.type
    });
    
    try {
        const response = await api.uploadFile('/products/1/photo', file);
        console.log('Upload success:', response);
    } catch (error) {
        console.error('Upload error:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack
        });
    }
}
```

**Common causes**:
- File too large (check backend max upload size)
- Wrong content type (ensure multipart/form-data)
- Missing file field name (should match backend expectation)

---

#### Issue: Data doesn't appear after API call

**Diagnostics**:
```javascript
async function loadData() {
    console.log('Starting data load...');
    
    try {
        const response = await api.get('/products');
        console.log('API Response:', response);
        console.log('Data:', response.data);
        console.log('Data length:', response.data?.length);
        
        if (!response.data) {
            console.error('No data in response');
            return;
        }
        
        response.data.forEach((item, index) => {
            console.log(`Processing item ${index}:`, item);
            displayItem(item);
        });
        
    } catch (error) {
        console.error('Error:', error);
    }
}
```

---

#### Issue: Form submits but data is wrong

**Solution**: Log data before sending:
```javascript
async function handleSubmit(e) {
    e.preventDefault();
    
    const data = collectFormData();
    
    // Debug: Log collected data
    console.log('Form data:', data);
    console.log('Data types:', {
        merchant_id: typeof data.merchant_id,
        price: typeof data.price,
        date: typeof data.date
    });
    
    // Validate before sending
    const errors = validateData(data);
    if (errors.length > 0) {
        console.error('Validation errors:', errors);
        alert(errors.join('\n'));
        return;
    }
    
    // Send to API
    await api.post('/endpoint', data);
}
```

---

### Performance Tips

#### 1. Debounce Search Input

Prevent excessive API calls during typing:

```javascript
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Usage
const searchInput = document.getElementById('search');
const debouncedSearch = debounce(async (query) => {
    const response = await api.get(`/products?search=${query}`);
    displayResults(response.data);
}, 300);

searchInput.addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});
```

---

#### 2. Cache API Responses

Reduce redundant API calls:

```javascript
const ApiCache = {
    cache: new Map(),
    ttl: 5 * 60 * 1000, // 5 minutes
    
    set: function(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    },
    
    get: function(key) {
        const cached = this.cache.get(key);
        
        if (!cached) return null;
        
        // Check if expired
        if (Date.now() - cached.timestamp > this.ttl) {
            this.cache.delete(key);
            return null;
        }
        
        return cached.data;
    },
    
    clear: function() {
        this.cache.clear();
    }
};

// Usage
async function getProducts() {
    const cached = ApiCache.get('products');
    if (cached) {
        return cached;
    }
    
    const response = await api.get('/products');
    ApiCache.set('products', response.data);
    return response.data;
}
```

---

#### 3. Lazy Load Images

Only load images when they're visible:

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});
```

---

## Best Practices Summary

### ✅ DO:
- ✅ Use `async/await` for API calls
- ✅ Validate data before sending to API
- ✅ Show loading states during API operations
- ✅ Handle errors gracefully with user-friendly messages
- ✅ Use event delegation for dynamic elements
- ✅ Parse numbers with `parseInt()` and `parseFloat()`
- ✅ Check for empty responses before processing
- ✅ Use data attributes instead of inline handlers
- ✅ Cache API responses when appropriate
- ✅ Debounce search inputs
- ✅ Log errors to console for debugging
- ✅ Provide clear user feedback

### ❌ DON'T:
- ❌ Use inline onclick handlers
- ❌ Forget to wrap in DOMContentLoaded
- ❌ Send string values when numbers are expected
- ❌ Ignore API errors
- ❌ Make API calls on every keystroke (use debounce)
- ❌ Forget to update dynamic counts/totals
- ❌ Skip client-side validation
- ❌ Hardcode API URLs in multiple places
- ❌ Forget to handle empty/null responses
- ❌ Leave console.logs in production code

---

## Quick Reference

### Essential Files Checklist
```
✅ js/config.js          - API configuration
✅ js/api.js             - API utility class
✅ js/template-loader.js - Navigation loader
✅ css/main.css          - CSS entry point
✅ All pages include required scripts
```

### Common Code Snippets

**Get URL Parameter**:
```javascript
const id = new URLSearchParams(window.location.search).get('id');
```

**Format Date**:
```javascript
const formatted = new Date(dateString).toLocaleDateString('en-GB');
```

**Format Currency**:
```javascript
const formatted = parseFloat(price).toFixed(2) + ' €';
```

**Show Alert**:
```javascript
alert('Message here');
```

**Redirect**:
```javascript
window.location.href = 'page.html';
```

---

## Conclusion

This guide provides everything needed to integrate the InfinExpense frontend with your backend API. Follow the patterns and examples provided, and refer back to this document when implementing new features.

### Next Steps

1. ✅ Set up your API backend with the endpoints described
2. ✅ Configure CORS on your backend
3. ✅ Update `js/config.js` with your API URL
4. ✅ Test API connectivity with a simple GET request
5. ✅ Implement one complete workflow (Merchant → Product → Receipt)
6. ✅ Test all CRUD operations
7. ✅ Add error handling and validation
8. ✅ Optimize with caching and debouncing
9. ✅ Deploy and test in production environment

### Support & Resources

- **Frontend Structure**: `/static/` folder
- **CSS Documentation**: `CSS_ORGANIZATION.md`
- **Backend Integration**: `BACKEND_INTEGRATION.md`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Cleanup Progress**: `CLEANUP_PROGRESS.md`

### Version History

- **v1.0** - November 14, 2025 - Initial comprehensive guide

---

**Happy Coding! 🚀**
