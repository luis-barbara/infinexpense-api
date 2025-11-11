# CSS Organization Guide

This document explains the organization and structure of `styles.css` for the InfinExpense project.

## Overview

The stylesheet is organized into **12 logical sections**, each handling specific component types. This structure makes it easy to:
- Find and modify styles quickly
- Maintain consistent design patterns
- Avoid CSS conflicts and repetition
- Collaborate with team members

**Total Lines**: ~857 lines  
**Backup**: `styles_old.css` (original unorganized version)

---

## Section Structure

### Section 1: RESET & BASE STYLES
**Lines**: 1-52  
**Purpose**: Foundation styles and CSS custom properties

**Contents**:
```css
/* Box model reset */
* { box-sizing: border-box; margin: 0; padding: 0; }

/* CSS Variables (Design Tokens) */
:root {
    --primary-color: #2563eb;     /* Blue */
    --success-color: #10b981;     /* Green */
    --danger-color: #ef4444;      /* Red */
    --warning-color: #f59e0b;     /* Orange */
    --secondary-color: #64748b;   /* Gray */
    --text-color: #1e293b;        /* Dark gray */
    --text-light: #64748b;        /* Light gray */
    --border-color: #e2e8f0;      /* Border gray */
    --background-color: #f8fafc;  /* Background */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}

/* Base body styles */
body { font-family: -apple-system, ...; }
```

**When to modify**:
- Changing color scheme
- Updating shadows or spacing
- Modifying default fonts

---

### Section 2: LAYOUT COMPONENTS
**Lines**: 53-147  
**Purpose**: Navigation, containers, and page structure

**Key Classes**:
- `.navbar` - Top navigation bar
  - `.nav-container` - Navigation wrapper
  - `.nav-brand` - Logo/brand text
  - `.nav-menu` - Navigation links list
  - `.nav-link` - Individual navigation links
  - `.nav-link.active` - Active page indicator

- `.container` - Main content wrapper (max-width: 1200px)

- `.page-header` - Page title section
  - `.page-title` - Main page heading
  - `.flex-between` - Flex utility for spacing

- Grid Layouts:
  - `.grid` - Generic grid container
  - `.grid-2` - 2-column grid
  - `.grid-3` - 3-column grid
  - `.stats-grid` - Responsive statistics grid (3 columns → 1 on mobile)

**When to modify**:
- Changing navigation design
- Adjusting page widths
- Modifying grid layouts

---

### Section 3: CARD COMPONENTS
**Lines**: 148-272  
**Purpose**: Card-based content containers

**Key Classes**:
- `.card` - Base card style (white background, shadow, rounded corners)

- Statistics Cards:
  - `.stat-card` - Individual stat display
  - `.stat-label` - Stat category label
  - `.stat-value` - Large numeric value
  - `.card-subtitle` - Additional info below value

- Receipt Cards:
  - `.receipt-card` - Receipt display card
  - `.receipt-header` - Top section with merchant/date
  - `.receipt-merchant` - Merchant name (bold)
  - `.receipt-date` - Receipt date
  - `.receipt-details` - Details section
  - `.receipt-detail-item` - Individual detail row
  - `.receipt-detail-label` - Detail label
  - `.receipt-detail-value` - Detail value

**When to modify**:
- Changing card appearance
- Adjusting spacing within cards
- Modifying hover effects

---

### Section 4: BUTTON COMPONENTS
**Lines**: 273-346  
**Purpose**: All button styles and variants

**Base Class**:
```css
.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
}
```

**Variants**:
- `.btn-primary` - Blue (primary actions)
- `.btn-secondary` - Gray (secondary actions)
- `.btn-success` - Green (success actions)
- `.btn-danger` - Red (delete/cancel)
- `.btn-outline` - Transparent with border

**Size Modifiers**:
- `.btn-sm` - Smaller buttons

**States**:
- `:hover` - Hover effects
- `:disabled` - Disabled state

**When to modify**:
- Creating new button variants
- Adjusting button sizes
- Changing hover effects

---

### Section 5: FORM COMPONENTS
**Lines**: 347-450 (estimated)  
**Purpose**: Form inputs, labels, and controls

**Key Classes**:
- Form Structure:
  - `.form-group` - Input group wrapper
  - `.form-label` - Input label

- Input Types:
  - `.form-input` - Text, number, date inputs
  - `.form-select` - Dropdown selects
  - `.form-textarea` - Multi-line text areas

- Search Components:
  - `.search-bar` - Search container (flex layout)
  - `.search-input` - Search text input

- File Upload:
  - `.file-upload` - Custom file upload styling
  - `.file-upload-label` - Upload button label
  - `.file-upload-text` - Selected file name display

**When to modify**:
- Changing input styles
- Adjusting form layouts
- Modifying validation states

---

### Section 6: LIST & TABLE COMPONENTS
**Lines**: 451-550 (estimated)  
**Purpose**: List items and table layouts

**Key Classes**:
- List Components:
  - `.list-container` - List wrapper
  - `.list-item` - Individual list item
  - `.list-item-main` - Main content area
  - `.list-item-label` - Field labels
  - `.list-item-value` - Field values
  - `.scrollable-list` - Fixed-height scrollable list

- Specific List Types:
  - `.receipt-item` - Receipt list items
  - `.product-item` - Product list items
  - `.category-item` - Category list items
  - `.merchant-item` - Merchant list items

- Table Components:
  - `.table-container` - Table wrapper
  - `.table` - Base table styles
  - `thead`, `tbody` - Table sections
  - `th`, `td` - Table cells

**When to modify**:
- Changing list layouts
- Adjusting table styles
- Modifying hover effects on items

---

### Section 7: PAGINATION & NAVIGATION
**Lines**: 551-620 (estimated)  
**Purpose**: Pagination controls

**Key Classes**:
- `.pagination` - Pagination wrapper (flex layout)
- `.pagination-btn` - Individual page buttons
- `.pagination-btn.active` - Current page
- `.pagination-btn:disabled` - Disabled state (prev/next)

**When to modify**:
- Changing pagination appearance
- Adjusting button spacing
- Modifying active state styles

---

### Section 8: DETAIL PAGE COMPONENTS
**Lines**: 621-680 (estimated)  
**Purpose**: Detail view specific components

**Key Classes**:
- `.detail-header` - Detail page header
- `.detail-title` - Detail page title
- `.detail-info` - Information grid
- `.detail-info-item` - Individual info field
- `.detail-info-label` - Field label
- `.detail-info-value` - Field value

- Receipt-specific:
  - `.receipt-products` - Products list section
  - `.product-row` - Individual product row
  - `.product-actions` - Action buttons for products

**When to modify**:
- Changing detail page layouts
- Adjusting info display
- Modifying edit interfaces

---

### Section 9: CHART & VISUALIZATION COMPONENTS
**Lines**: 681-730 (estimated)  
**Purpose**: Chart.js containers and image displays

**Key Classes**:
- `.chart-container` - Chart wrapper
- `.chart-title` - Chart heading
- `canvas` - Chart.js canvas element

- Image Display:
  - `.image-preview` - Receipt image display
  - `.image-preview img` - Image styling

**When to modify**:
- Adjusting chart sizes
- Changing chart titles
- Modifying image displays

---

### Section 10: BADGES & STATUS INDICATORS
**Lines**: 731-780 (estimated)  
**Purpose**: Status badges and labels

**Key Classes**:
- `.badge` - Base badge style
- `.badge-primary` - Blue badge
- `.badge-success` - Green badge
- `.badge-warning` - Orange badge
- `.badge-danger` - Red badge
- `.badge-secondary` - Gray badge

**Usage Examples**:
```html
<span class="badge badge-success">Paid</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-danger">Overdue</span>
```

**When to modify**:
- Creating new status types
- Changing badge colors
- Adjusting badge sizes

---

### Section 11: UTILITY CLASSES
**Lines**: 781-820 (estimated)  
**Purpose**: Helper classes for common patterns

**Key Classes**:
- Text Alignment:
  - `.text-center` - Center text
  - `.text-right` - Right-align text
  - `.text-left` - Left-align text

- Spacing:
  - `.mb-1`, `.mb-2`, `.mb-3` - Margin bottom
  - `.mt-1`, `.mt-2`, `.mt-3` - Margin top
  - `.p-1`, `.p-2`, `.p-3` - Padding

- Flexbox:
  - `.flex-between` - justify-content: space-between
  - `.flex-center` - Center items
  - `.flex-column` - Flex direction column

- Colors:
  - `.text-primary` - Primary color text
  - `.text-success` - Success color text
  - `.text-danger` - Danger color text

- Font Weights:
  - `.font-bold` - Bold text
  - `.font-semibold` - Semi-bold text

**When to modify**:
- Adding new utility classes
- Creating spacing scale
- Extending color utilities

---

### Section 12: RESPONSIVE DESIGN
**Lines**: 821-857  
**Purpose**: Mobile-first responsive styles

**Breakpoint**: `@media (max-width: 768px)`

**Modified Components**:
- `.stats-grid` - 3 columns → 1 column
- `.grid-2`, `.grid-3` - Multi-column → 1 column
- `.navbar` - Simplified navigation
- `.page-header` - Stacked layout
- `.list-item` - Adjusted spacing
- `.receipt-card` - Improved mobile display
- `.table` - Horizontal scroll enabled

**When to modify**:
- Adjusting breakpoints
- Adding tablet-specific styles
- Improving mobile UX

---

## CSS Variables Reference

All colors and common values are defined as CSS variables in Section 1.

### Color Variables
```css
--primary-color: #2563eb;
--success-color: #10b981;
--danger-color: #ef4444;
--warning-color: #f59e0b;
--secondary-color: #64748b;
--text-color: #1e293b;
--text-light: #64748b;
--border-color: #e2e8f0;
--background-color: #f8fafc;
```

### Shadow Variables
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
```

### Usage in Styles
```css
.card {
    background: white;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
}

.btn-primary {
    background: var(--primary-color);
}
```

---

## Naming Conventions

### BEM-Inspired Pattern
```css
.block { }              /* Component */
.block__element { }     /* Child element */
.block--modifier { }    /* Variant */
```

**Examples**:
```css
.receipt-card { }               /* Block */
.receipt-card__header { }       /* Element */
.receipt-card--highlighted { }  /* Modifier */
```

### Simplified Class Names (Used in this project)
```css
.receipt-card { }        /* Parent component */
.receipt-header { }      /* Child (scoped by context) */
.receipt-merchant { }    /* Specific element */
```

---

## Best Practices

### 1. Use CSS Variables
✅ **Do this**:
```css
.btn-primary {
    background: var(--primary-color);
}
```

❌ **Not this**:
```css
.btn-primary {
    background: #2563eb;
}
```

### 2. Group Related Selectors
✅ **Do this**:
```css
/* Receipt Card Components */
.receipt-card { }
.receipt-header { }
.receipt-merchant { }
.receipt-date { }
```

### 3. Use Consistent Spacing
- Padding: 0.5rem, 1rem, 1.5rem, 2rem
- Margin: 0.5rem, 1rem, 1.5rem, 2rem
- Gap: 0.5rem, 1rem, 1.5rem

### 4. Comment Complex Sections
```css
/* Grid layout: 3 columns on desktop, 1 on mobile */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}
```

### 5. Mobile-First Approach
Write base styles for mobile, then add desktop enhancements:
```css
/* Mobile-first (default) */
.grid-3 {
    display: grid;
    grid-template-columns: 1fr;
}

/* Desktop enhancement */
@media (min-width: 769px) {
    .grid-3 {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

---

## Common Modifications

### Change Primary Color
1. Update `--primary-color` in Section 1
2. All buttons, links, and accents update automatically

### Add New Button Variant
Add to Section 4:
```css
.btn-info {
    background: #3b82f6;
    color: white;
}

.btn-info:hover {
    background: #2563eb;
}
```

### Add New Utility Class
Add to Section 11:
```css
.mt-4 {
    margin-top: 2rem;
}
```

### Adjust Mobile Breakpoint
Modify Section 12:
```css
/* Change from 768px to 1024px */
@media (max-width: 1024px) {
    /* ... */
}
```

---

## Maintenance Checklist

- [ ] Keep backup file (`styles_old.css`) for reference
- [ ] Document new sections if adding 50+ lines
- [ ] Use CSS variables for repeated values
- [ ] Test mobile responsiveness after changes
- [ ] Validate CSS (W3C validator)
- [ ] Check browser compatibility (Can I Use)
- [ ] Minify for production (cssnano, clean-css)

---

## Performance Notes

- **File Size**: ~857 lines (~30KB unminified)
- **Minified**: ~15-20KB (estimated)
- **Gzipped**: ~5-8KB (estimated)
- **Load Time**: <50ms on average connection

**Optimization Tips**:
1. Remove unused styles before production
2. Minify CSS for production
3. Consider critical CSS for above-the-fold content
4. Use CSS variables instead of repeated values

---

## Browser Support

**Target Browsers**:
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile Safari: iOS 12+
- Chrome Mobile: Latest

**CSS Features Used**:
- CSS Grid (supported in all modern browsers)
- CSS Variables (not supported in IE11)
- Flexbox (fully supported)
- CSS Transitions (fully supported)

---

## Migration from Old Structure

The original `styles.css` had no clear organization. Here's how it was restructured:

**Before** (styles_old.css):
- Mixed component styles
- No clear sections
- Repeated values
- Hard to find specific styles

**After** (styles.css):
- 12 clear sections with headers
- CSS variables for common values
- Logical grouping
- Easy navigation and maintenance

**To revert**: Replace `styles.css` with `styles_old.css`

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintained By**: ETIC Algarve - Base de Dados Course
