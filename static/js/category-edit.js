import { getCategories, updateCategory, deleteCategory } from '../api/categories_api.js';

let currentCategoryId = null;

/**
 * Get category ID from URL
 */
function getCategoryIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id'));
}

/**
 * Load and populate category
 */
async function loadCategory() {
    try {
        currentCategoryId = getCategoryIdFromUrl();
        
        if (!currentCategoryId) {
            alert('No category ID provided');
            window.location.href = 'list.html';
            return;
        }
        
        const categories = await getCategories();
        const category = categories.find(c => c.id === currentCategoryId);
        
        if (!category) {
            alert('Category not found');
            window.location.href = 'list.html';
            return;
        }
        
        // Populate form
        document.getElementById('categoryName').value = category.name;
        
        // Disable delete button if category has items
        const deleteBtn = document.getElementById('deleteBtn');
        if (category.item_count > 0) {
            deleteBtn.disabled = true;
            deleteBtn.title = `Cannot delete category with ${category.item_count} items`;
            deleteBtn.style.opacity = '0.5';
            deleteBtn.style.cursor = 'not-allowed';
        }
    } catch (error) {
        console.error('Error loading category:', error);
        alert('Error loading category');
    }
}

/**
 * Handle form submission
 */
document.getElementById('categoryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('categoryName').value.trim();
    
    if (!name) {
        alert('Please enter a category name');
        return;
    }
    
    try {
        await updateCategory(currentCategoryId, { name });
        alert('Category updated successfully!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Error updating category:', error);
        alert(`Error: ${error.message}`);
    }
});

/**
 * Handle delete button
 */
document.getElementById('deleteBtn').addEventListener('click', async () => {
    try {
        const categories = await getCategories();
        const category = categories.find(c => c.id === currentCategoryId);
        
        if (category.item_count > 0) {
            alert(`Cannot delete category with ${category.item_count} items. Please remove all items first.`);
            return;
        }
        
        if (confirm('Are you sure you want to delete this category?')) {
            await deleteCategory(currentCategoryId);
            alert('Category deleted successfully!');
            window.location.href = 'list.html';
        }
    } catch (error) {
        console.error('Error deleting category:', error);
        alert(`Error: ${error.message}`);
    }
});

document.addEventListener('DOMContentLoaded', loadCategory);