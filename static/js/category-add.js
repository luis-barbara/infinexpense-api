import { createCategory } from '../api/categories_api.js';

/**
 * Handle category form submission.
 */
document.getElementById('categoryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nameInput = document.getElementById('categoryName');
    const name = nameInput.value.trim();
    
    if (!name) {
        alert('Please enter a category name');
        return;
    }
    
    try {
        const newCategory = await createCategory({ name });
        alert(`Category "${name}" created successfully!`);
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Error creating category:', error);
        alert(`Error: ${error.message}`);
    }
});