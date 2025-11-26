import { getProductById, updateProduct } from '/static/api/products_api.js';
import { getCategories } from '/static/api/categories_api.js';
import { getMeasurementUnits } from '/static/api/measurement_units_api.js';
import { uploadProductPhoto } from '/static/api/uploads_api.js';

let currentProductId = null;
let currentProduct = null;
let allCategories = [];
let allUnits = [];
let pendingPhotoRemoval = false;
let pendingPhotoFile = null;
let pendingPhotoPreview = null;


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
        return true;
    } catch (error) {
        console.error('Error loading categories:', error);
        return false;
    }
}

/**
 * Load measurement units for dropdown
 */
async function loadMeasurementUnits() {
    try {
        allUnits = await getMeasurementUnits();
        return true;
    } catch (error) {
        console.error('Error loading measurement units:', error);
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

        // Load dropdowns first
        await loadCategories();
        await loadMeasurementUnits();

        // Populate dropdowns
        populateCategorySelect();
        populateVolumeSelect();

        // Then load product
        currentProduct = await getProductById(currentProductId);

        // Update page title
        const titleEl = document.querySelector('h1.gradient-text');
        if (titleEl) {
            titleEl.textContent = `Edit Product: ${currentProduct.name}`;
        }

        // Populate form
        populateForm(currentProduct);
    } catch (error) {
        console.error('Error loading product:', error);
        alert('Error loading product: ' + error.message);
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
    }
    
    // Category
    const categorySelect = form.querySelector('select[name="category"]');
    if (categorySelect && product.category_id) {
        categorySelect.value = product.category_id;
    }
    
    // Volume/Measurement Unit
    const volumeSelect = form.querySelector('select[name="volume"]');
    if (volumeSelect && product.measurement_unit_id) {
        volumeSelect.value = product.measurement_unit_id;
    }
    
    // Barcode
    const barcodeInput = form.querySelector('input[name="barcode"]');
    if (barcodeInput) {
        barcodeInput.value = product.barcode || '';
    }
    
    // Image 
    displayCurrentPhoto(product.product_list_photo);

    // Reset all pending photo changes
    pendingPhotoRemoval = false;
    pendingPhotoFile = null;
    pendingPhotoPreview = null;

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

        // Handle photo removal if pending
        if (pendingPhotoRemoval) {
            updateData.product_list_photo = null;
        };
        
        await updateProduct(currentProductId, updateData);

        if (pendingPhotoFile && !pendingPhotoRemoval) {
            try {
                const updatedProduct = await uploadProductPhoto(currentProductId, pendingPhotoFile);
            } catch (photoError) {
                console.error('Error uploading photo:', photoError);
                alert('Product saved but photo upload failed: ' + photoError.message);
            }
        }

        alert('Produto atualizado com sucesso!');
        window.location.href = `/static/product/view.html?id=${currentProductId}`;
    } catch (error) {
        console.error('Error updating product:', error);
        alert('Error updating product: ' + error.message);
    }
}

/**
 * Cancel edit
 */
function cancelEdit() {
    window.location.href = `/static/product/view.html?id=${currentProductId}`;
}



// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProduct();

    // Photo upload file input change
    const photoInput = document.getElementById('photoUpload');
    if (photoInput) {
        photoInput.addEventListener('change', function() {
            if (this.files[0]) {
                uploadPhoto(); // Automatically upload when file is selected
            }
        });
    }

});

// Expose to global scope
window.cancelEdit = cancelEdit;


/**
 * Display current photo if exists
 */
function displayCurrentPhoto(photoPath) {
    const container = document.getElementById('currentPhotoContainer');
    const img = document.getElementById('currentPhoto');
    const uploadArea = document.getElementById('photoUploadArea');
    
    // Show pending photo if exists, otherwise show current photo
    const displayPath = pendingPhotoPreview || photoPath;
    const shouldShowPhoto = (displayPath && !pendingPhotoRemoval) || pendingPhotoFile;
    
    if (shouldShowPhoto) {
        if (pendingPhotoFile) {
            // Show pending photo preview
            img.src = pendingPhotoPreview;
        } else {
            // Show current photo
            img.src = photoPath;
        }
        container.style.display = 'flex';
        uploadArea.style.display = 'none';
    } else {
        container.style.display = 'none';
        uploadArea.style.display = 'flex';
        
        // Update upload area text based on state
        const uploadLabel = document.getElementById('photoUploadLabel');
        if (uploadLabel) {
            if (pendingPhotoRemoval && currentProduct.product_list_photo) {
                uploadLabel.innerHTML = `
                    <div class="photo-upload-icon">⚠️</div>
                    <div class="photo-upload-text">Photo will be removed</div>
                `;
            } else {
                uploadLabel.innerHTML = `
                    <div class="photo-upload-icon">📷</div>
                    <div class="photo-upload-text">Upload Photo</div>
                `;
            }
        }
    }
}

/**
 * Trigger photo upload by clicking the hidden file input
 */
function triggerPhotoUpload() {
    if (!confirm('Are you sure you want to change the photo?')) return;
    const fileInput = document.getElementById('photoUpload');
    fileInput.click();
}

/**
 * Upload photo for receipt (stage for later upload)
 */
async function uploadPhoto() {
    const fileInput = document.getElementById('photoUpload');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a photo first');
        return;
    }
    
    // Stage the file for upload when Save Changes is clicked
    pendingPhotoFile = file;
    pendingPhotoRemoval = false; // Clear any pending removal
    
    // Create preview URL
    const reader = new FileReader();
    reader.onload = function(e) {
        pendingPhotoPreview = e.target.result;
        displayCurrentPhoto(currentProduct.product_list_photo);
    };
    reader.readAsDataURL(file);
    
    // Clear file input
    fileInput.value = '';
    
    alert('Photo staged for upload. Click "Save Changes" to apply.');
}

/**
 * Remove current photo (staged until Save Changes)
 */
function removeCurrentPhoto() {
    if (!confirm('Are you sure you want to remove this photo? Changes will be saved when you click "Save Changes".')) return;
    
    // Clear any pending photo upload
    pendingPhotoFile = null;
    pendingPhotoPreview = null;
    
    // Mark photo for removal but don't delete from database yet
    pendingPhotoRemoval = true;
    
    // Update UI
    displayCurrentPhoto(currentProduct.product_list_photo);
    
    alert('Photo marked for removal. Click "Save Changes" to apply.');
}

// Expose photo functions to global scope
window.uploadPhoto = uploadPhoto;
window.removeCurrentPhoto = removeCurrentPhoto;
window.triggerPhotoUpload = triggerPhotoUpload;