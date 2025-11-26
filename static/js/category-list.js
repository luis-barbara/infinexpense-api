import { getCategories, deleteCategory } from '/static/api/categories_api.js';

let allCategories = [];
let categoryChart = null;

window.handleDeleteCategory = handleDeleteCategory;

/**
 * Initialize the categories page.
 */
async function initializePage() {
    await loadCategories();
    setupEventListeners();
}

/**
 * Fetch categories from backend and render them.
 */
async function loadCategories() {
    try {
        const categories = await getCategories();
        allCategories = categories;
        renderCategoriesList();
        renderChart();
    } catch (error) {
        console.error('Error loading categories:', error);
        showError('Failed to load categories');
    }
}

/**
 * Render the categories list.
 */
function renderCategoriesList() {
    const container = document.getElementById('categoriesList');
    if (!container) return;
    
    if (allCategories.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: #666;">No categories found</p>';
        return;
    }
    
    container.innerHTML = allCategories.map(category => {
        const itemPercentage = category.item_percentage || 0;
        const color = category.color || '#999999';
        
        return `
            <div style="display: grid; grid-template-columns: 30px 1fr 1fr 0.8fr 1fr 0.8fr; gap: 1rem; padding: 0.75rem; border-bottom: 1px solid hsl(var(--border) / 0.2); align-items: center;">
                <div class="category-color-box" style="background-color: ${color}; width: 24px; height: 24px; border-radius: 4px;"></div>
                <div class="category-name">${category.name}</div>
                <div class="category-meta">${category.item_count || 0} Items</div>
                <div class="category-meta">${itemPercentage}%</div>
                <div style="color: hsl(var(--primary)); font-weight: 500; font-size: 0.9rem;">${(category.total_spent || 0).toFixed(2)} €</div>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="/static/category/edit.html?id=${category.id}" class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 0.3rem 0.6rem;" title="Edit">✏️</a>
                    <button class="btn btn-danger btn-sm" style="font-size: 0.7rem; padding: 0.3rem 0.6rem;" title="Delete" onclick="handleDeleteCategory(${category.id})">🗑️</button>
                </div>
            </div>
        `;
    }).join('');
}


/**
 * Render the pie chart.
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
                    color: document.documentElement.getAttribute('data-theme') === 'light' ? '#000000' : '#ffffff',
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
                    offset: 10,
                    distance: 45
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
 * Handle category deletion.
 */
async function handleDeleteCategory(id) {
    try {
        const category = allCategories.find(c => c.id === id);
        
        if (!category) {
            showError('Category not found');
            return;
        }
        
        if (category.item_count > 0) {
            showError(`Cannot delete category with ${category.item_count} items. Please remove all items first.`);
            return;
        }
        
        if (!confirm('Are you sure you want to delete this category?')) {
            return;
        }
        
        await deleteCategory(id);
        await loadCategories();
        showSuccess('Category deleted successfully');
    } catch (error) {
        console.error('Error deleting category:', error);
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
    
    // Search button
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', handleSearch);
    }
    
    // Date filter buttons
    const applyFilterBtn = document.getElementById('applyFilterBtn');
    const resetFilterBtn = document.getElementById('resetFilterBtn');
    
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', handleDateFilter);
    }
    
    if (resetFilterBtn) {
        resetFilterBtn.addEventListener('click', handleResetFilter);
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
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

/**
 * Handle date range filter
 */
async function handleDateFilter() {
    const startInput = document.getElementById('startDate');
    const endInput = document.getElementById('endDate');
    
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
            console.log('Filtering with dates:', { start_date: startDate, end_date: endDate });
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
            showError(`Failed to filter categories: ${error.message}`);
        }
    }
}

/**
 * Reset date filter and load all categories
 */
async function handleResetFilter() {
    const startInput = document.getElementById('startDate');
    const endInput = document.getElementById('endDate');
    
    // Reset to current month
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    startInput.value = firstDay.toISOString().split('T')[0];
    endInput.value = lastDay.toISOString().split('T')[0];
    
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

document.addEventListener('DOMContentLoaded', initializePage);