import { getProductById, updateProduct } from '../api/products_api.js';
import { getCategories } from '../api/categories_api.js';
import { getMeasurementUnits } from '../api/measurement_units_api.js';

let currentProductId = null;
let currentProduct = null;
let allCategories = [];
let allUnits = [];

/**
 * Get product ID from URL
 */
function getProductIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Load categories for dropdown
 */
async function loadCategories() {
    try {
        allCategories = await getCategories();
        console.log('Categories loaded:', allCategories.length);
        return true;
    } catch (error) {
        console.error('Erro ao carregar categorias:', error);
        return false;
    }
}

/**
 * Load measurement units for dropdown
 */
async function loadMeasurementUnits() {
    try {
        allUnits = await getMeasurementUnits();
        console.log('Measurement units loaded:', allUnits.length);
        return true;
    } catch (error) {
        console.error('Erro ao carregar unidades de medida:', error);
        return false;
    }
}

/**
 * Populate category select
 */
function populateCategorySelect() {
    const select = document.querySelector('select[name="category"]');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select a category</option>';
    allCategories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        select.appendChild(option);
    });
}

/**
 * Populate volume select
 */
function populateVolumeSelect() {
    const select = document.querySelector('select[name="volume"]');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select volume</option>';
    allUnits.forEach(unit => {
        const option = document.createElement('option');
        option.value = unit.id;
        option.textContent = `${unit.abbreviation} (${unit.name})`;
        select.appendChild(option);
    });
}

/**
 * Load product and populate form
 */
async function loadProduct() {
    try {
        currentProductId = getProductIdFromUrl();
        if (!currentProductId) {
            alert('Product ID not provided');
            window.location.href = 'list.html';
            return;
        }

        console.log('Loading product ID:', currentProductId);

        // Load dropdowns first
        await loadCategories();
        await loadMeasurementUnits();

        // Populate dropdowns
        populateCategorySelect();
        populateVolumeSelect();

        // Then load product
        currentProduct = await getProductById(currentProductId);
        console.log('Product loaded:', currentProduct);

        // Update page title
        document.querySelector('.page-title').textContent = `Edit Product: ${currentProduct.name}`;

        // Populate form
        populateForm(currentProduct);
    } catch (error) {
        console.error('Erro ao carregar produto:', error);
        alert('Erro ao carregar produto: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate form with product data
 */
function populateForm(product) {
    const form = document.querySelector('form');
    
    // Product name
    const nameInput = form.querySelector('input[name="name"]');
    if (nameInput) {
        nameInput.value = product.name;
        console.log('Set product name to:', product.name);
    }
    
    // Category
    const categorySelect = form.querySelector('select[name="category"]');
    if (categorySelect && product.category_id) {
        categorySelect.value = product.category_id;
        console.log('Set category to:', product.category_id);
    }
    
    // Volume/Measurement Unit
    const volumeSelect = form.querySelector('select[name="volume"]');
    if (volumeSelect && product.measurement_unit_id) {
        volumeSelect.value = product.measurement_unit_id;
        console.log('Set volume to:', product.measurement_unit_id);
    }
    
    // Barcode
    const barcodeInput = form.querySelector('input[name="barcode"]');
    if (barcodeInput) {
        barcodeInput.value = product.barcode || '';
        console.log('Set barcode to:', product.barcode);
    }
    
    // Add form submit listener
    form.addEventListener('submit', handleSubmit);
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    try {
        const form = document.querySelector('form');
        const nameInput = form.querySelector('input[name="name"]');
        const categorySelect = form.querySelector('select[name="category"]');
        const volumeSelect = form.querySelector('select[name="volume"]');
        const barcodeInput = form.querySelector('input[name="barcode"]');
        
        if (!nameInput.value) {
            alert('Product name is required');
            return;
        }
        
        if (!categorySelect.value) {
            alert('Category is required');
            return;
        }
        
        if (!volumeSelect.value) {
            alert('Volume is required');
            return;
        }
        
        const updateData = {
            name: nameInput.value,
            category_id: parseInt(categorySelect.value),
            measurement_unit_id: parseInt(volumeSelect.value),
            barcode: barcodeInput.value || null
        };
        
        console.log('Updating product:', updateData);
        await updateProduct(currentProductId, updateData);
        
        alert('Produto atualizado com sucesso!');
        window.location.href = `view.html?id=${currentProductId}`;
    } catch (error) {
        console.error('Erro ao atualizar produto:', error);
        alert('Erro ao atualizar produto: ' + error.message);
    }
}

/**
 * Cancel edit
 */
function cancelEdit() {
    window.location.href = `view.html?id=${currentProductId}`;
}

// Expose to global scope
window.cancelEdit = cancelEdit;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProduct();
});