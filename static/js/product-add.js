import { createProduct } from '../api/products_api.js';
import { getCategories } from '../api/categories_api.js';
import { getMeasurementUnits } from '../api/measurement_units_api.js';

let allCategories = [];
let allUnits = [];
let selectedPhotoFile = null;

/**
 * Load categories for dropdown
 */
async function loadCategories() {
    try {
        allCategories = await getCategories();
        populateCategorySelect();
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
        populateVolumeSelect();
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
 * Handle photo file selection
 */
function handlePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    selectedPhotoFile = file;
    console.log('Photo selected:', file.name);
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(event) {
        const preview = document.querySelector('.photo-upload-label-content');
        if (preview) {
            preview.innerHTML = `<img src="${event.target.result}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">`;
        }
    };
    reader.readAsDataURL(file);
}

/**
 * Upload photo to server
 */
async function uploadPhoto(productId) {
    if (!selectedPhotoFile) return null;
    
    try {
        const formData = new FormData();
        formData.append('file', selectedPhotoFile);
        
        const response = await fetch(`http://localhost:8000/products/${productId}/upload-photo`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to upload photo');
        }
        
        console.log('Photo uploaded successfully');
        return true;
    } catch (error) {
        console.error('Erro ao carregar foto:', error);
        return false;
    }
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    try {
        const form = document.querySelector('form');
        const nameInput = form.querySelector('input[type="text"]');
        const categorySelect = form.querySelector('select[name="category"]') || form.querySelectorAll('select')[0];
        const volumeSelect = form.querySelector('select[name="volume"]') || form.querySelectorAll('select')[1];
        const barcodeInput = form.querySelector('input[placeholder*="barcode"]');
        
        // Validation
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
        
        const newProduct = {
            name: nameInput.value,
            category_id: parseInt(categorySelect.value),
            measurement_unit_id: parseInt(volumeSelect.value),
            barcode: barcodeInput.value || null
        };
        
        console.log('Creating product:', newProduct);
        const createdProduct = await createProduct(newProduct);
        console.log('Product created:', createdProduct);
        
        // Upload photo if selected
        if (selectedPhotoFile) {
            await uploadPhoto(createdProduct.id);
        }
        
        alert('Produto criado com sucesso!');
        window.location.href = `view.html?id=${createdProduct.id}`;
    } catch (error) {
        console.error('Erro ao criar produto:', error);
        alert('Erro ao criar produto: ' + error.message);
    }
}

/**
 * Cancel add
 */
function cancelAdd() {
    window.location.href = 'list.html';
}

// Expose to global scope
window.cancelAdd = cancelAdd;
window.handlePhotoSelect = handlePhotoSelect;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async function() {
    await loadCategories();
    await loadMeasurementUnits();
    
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    // Handle photo input
    const photoInput = document.getElementById('product-photo');
    if (photoInput) {
        photoInput.addEventListener('change', handlePhotoSelect);
    }
});