// static/js/categories_api.js

const API_BASE_URL = "http://localhost:8000/categories"; 

/**
 * GET: List all categories with optional pagination
 */
async function getCategories(skip = 0, limit = 100) {
    try {
        const response = await fetch(`${API_BASE_URL}?skip=${skip}&limit=${limit}`);
        if (!response.ok) throw new Error("Failed to fetch categories");
        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

/**
 * GET: Get a single category by ID
 */
async function getCategoryById(categoryId) {
    try {
        const response = await fetch(`${API_BASE_URL}/${categoryId}`);
        if (!response.ok) throw new Error("Category not found");
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

/**
 * POST: Create a new category
 */
async function createCategory(name) {
    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to create category");
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

/**
 * PUT: Update an existing category
 */
async function updateCategory(categoryId, name) {
    try {
        const response = await fetch(`${API_BASE_URL}/${categoryId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to update category");
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

/**
 * DELETE: Delete a category by ID
 */
async function deleteCategory(categoryId) {
    try {
        const response = await fetch(`${API_BASE_URL}/${categoryId}`, {
            method: "DELETE"
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to delete category");
        }
        return true;
    } catch (error) {
        console.error(error);
        return false;
    }
}

/**
 * Example usage:
 * getCategories().then(console.log);
 * createCategory("Fruits").then(console.log);
 * updateCategory(1, "Vegetables").then(console.log);
 * deleteCategory(2).then(console.log);
 */
