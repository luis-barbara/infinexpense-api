import { getCategories, deleteCategory } from '../api/categories_api.js';

let allCategories = [];
let categoryChart = null;

// Make function globally available
window.handleDeleteCategory = handleDeleteCategory;

/**
 * Initialize the categories page
 */
async function initializePage() {
    await loadCategories();
    setupEventListeners();
}

/**
 * Fetch categories from backend and render them
 */
async function loadCategories() {
    try {
        const categories = await getCategories();
        allCategories = categories;
        console.log('Full API response:', categories);  // Log entire response
        console.log('First category:', categories[0]);  // Log first category object
        renderCategoriesList();
        renderChart();
    } catch (error) {
        console.error('Error loading categories:', error);
        showError('Failed to load categories');
    }
}

/**
 * Render the categories list
 */
function renderCategoriesList() {
    const container = document.getElementById('categoriesList');
    
    if (!container) {
        console.error('Categories list container not found');
        return;
    }
    
    if (allCategories.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: #666;">No categories found</p>';
        return;
    }
    
    container.innerHTML = allCategories.map(category => {
        const itemPercentage = category.item_percentage || 0;
        const color = category.color;
        
        return `
            <div class="list-item list-item-compact">
                <div class="list-item-main categories-list-grid">
                    <div class="category-color-box" style="background-color: ${color};"></div>
                    <div class="category-name">${category.name}</div>
                    <div class="category-meta">${category.item_count || 0} Items</div>
                    <div class="category-meta">${itemPercentage}%</div>
                    <div style="color: var(--primary-color); font-weight: 500; font-size: 0.95rem; text-align: center;">${(category.total_spent || 0).toFixed(2)} €</div>
                    <div class="list-item-actions">
                        <a href="edit.html?id=${category.id}" class="btn btn-secondary btn-sm" title="Edit">✏️</a>
                        <button class="btn btn-danger btn-sm" title="Delete" onclick="handleDeleteCategory(${category.id})">🗑️</button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Render the pie chart
 */
function renderChart() {
    const ctx = document.getElementById('categoryChart');
    
    if (!ctx) {
        console.error('Chart canvas not found');
        return;
    }
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    const labels = allCategories.map(c => c.name);
    const data = allCategories.map(c => c.total_spent || 0);
    const backgroundColor = allCategories.map(c => c.color);
    
    categoryChart = new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderWidth: 1,
                borderColor: '#000000ff',
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            layout: {
                padding: {
                    top: 30,
                    bottom: 40,
                    left: 20,
                    right: 20
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 16,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return context[0].label;
                        },
                        label: function(context) {
                            const value = context.parsed.toFixed(2);
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return [percentage + '%', value + ' €'];
                        }
                    }
                },
                datalabels: {
                    color: '#000000ff',
                    font: {
                        weight: 'bold',
                        size: 12
                    },
                    formatter: function(value, context) {
                        return context.chart.data.labels[context.dataIndex];
                    },
                    textAlign: 'center',
                    anchor: 'end',
                    align: 'end',
                    offset: 5,
                    distance: 25
                },
                datalabelsInside: {
                    color: '#ffffff',
                    font: {
                        weight: 'bold',
                        size: 11
                    },
                    formatter: function(value, context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return percentage + '%';
                    },
                    anchor: 'center',
                    align: 'center'
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true
            }
        },
        plugins: [ChartDataLabels]
    });
}

/**
 * Handle category deletion
 */
async function handleDeleteCategory(id) {
    try {
        const category = allCategories.find(c => c.id === id);
        
        if (!category) {
            showError('Category not found');
            return;
        }
        
        // Check if category has items (products)
        if (category.item_count > 0) {
            showError(`Cannot delete category with ${category.item_count} items. Please remove all items first.`);
            return;
        }
        
        // Confirm deletion
        if (!confirm('Are you sure you want to delete this category?')) {
            return;
        }
        
        // Attempt to delete
        await deleteCategory(id);
        
        // If deletion was successful, reload categories
        await loadCategories();
        showSuccess('Category deleted successfully');
    } catch (error) {
        console.error('Error deleting category:', error);
        
        // Check if error is due to associated data
        if (error.message.includes('foreign key') || error.message.includes('associated')) {
            showError('Cannot delete category with associated receipts. Please remove all items first.');
        } else {
            showError(`Failed to delete category: ${error.message}`);
        }
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Search filter
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
    
    // Date filter
    const filterBars = document.querySelectorAll('.search-bar');
    const dateFilterBar = filterBars[filterBars.length - 1];
    const applyFilterBtn = dateFilterBar.querySelector('.btn-primary');
    const resetBtn = dateFilterBar.querySelector('.btn-secondary');
    
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', handleDateFilter);
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', handleResetFilter);
    }
}

/**
 * Handle search filter
 */
function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    const container = document.getElementById('categoriesList');
    const items = container.querySelectorAll('.list-item');
    
    items.forEach(item => {
        const categoryName = item.querySelector('.category-name').textContent.toLowerCase();
        
        if (categoryName.includes(searchTerm)) {
            item.style.display = '';  // Show
        } else {
            item.style.display = 'none';  // Hide
        }
    });
}

/**
 * Handle date range filter
 */
async function handleDateFilter() {
    const filterBars = document.querySelectorAll('.search-bar');
    const dateFilterBar = filterBars[filterBars.length - 1];
    
    const dateInputs = dateFilterBar.querySelectorAll('input[type="date"]');
    const startInput = dateInputs[0];
    const endInput = dateInputs[1];
    
    if (startInput && endInput) {
        const startDate = startInput.value;
        const endDate = endInput.value;
        
        if (!startDate || !endDate) {
            showError('Please select both start and end dates');
            return;
        }
        
        if (new Date(startDate) > new Date(endDate)) {
            showError('Start date must be before end date');
            return;
        }
        
        try {
            const categories = await getCategories({
                start_date: startDate,
                end_date: endDate
            });
            allCategories = categories;
            renderCategoriesList();
            renderChart();
            showSuccess(`Showing spending from ${startDate} to ${endDate}`);
        } catch (error) {
            console.error('Error filtering categories:', error);
            showError('Failed to filter categories by date');
        }
    }
}

/**
 * Reset date filter and load all categories
 */
async function handleResetFilter() {
    const filterBars = document.querySelectorAll('.search-bar');
    const dateFilterBar = filterBars[filterBars.length - 1];
    
    const dateInputs = dateFilterBar.querySelectorAll('input[type="date"]');
    dateInputs[0].value = '';
    dateInputs[1].value = '';
    
    try {
        const categories = await getCategories();
        allCategories = categories;
        renderCategoriesList();
        renderChart();
        showSuccess('Filter reset - showing all categories');
    } catch (error) {
        console.error('Error resetting filter:', error);
        showError('Failed to reset filter');
    }
}

/**
 * Show error message
 */
function showError(message) {
    console.error(message);
    
    // Show alert to user
    alert(`${message}`);
    
    // Or show toast notification if you have one
    // showToast(message, 'error');
}

/**
 * Show success message
 */
function showSuccess(message) {
    console.log(message);
    
    // Show alert to user
    alert(`${message}`);
    
    // Or show toast notification if you have one
    // showToast(message, 'success');
}

// Initialize page on load
document.addEventListener('DOMContentLoaded', initializePage);