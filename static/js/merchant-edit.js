import { getMerchantById, updateMerchant, deleteMerchant, uploadMerchantPhoto } from '../api/merchants_api.js';

let currentMerchantId = null;
let currentMerchant = null;
let selectedPhotoFile = null;

/**
 * Get merchant ID from URL
 */
function getMerchantIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Load merchant and populate form
 */
async function loadMerchant() {
    try {
        currentMerchantId = getMerchantIdFromUrl();
        if (!currentMerchantId) {
            alert('Merchant ID not provided');
            window.location.href = 'list.html';
            return;
        }

        currentMerchant = await getMerchantById(currentMerchantId);

        // Update page title
        document.querySelector('.page-title').textContent = `Edit Merchant: ${currentMerchant.name}`;

        // Populate form
        populateForm(currentMerchant);
    } catch (error) {
        console.error('Error loading merchant:', error);
        alert('Error loading merchant: ' + error.message);
        window.location.href = 'list.html';
    }
}

/**
 * Populate form with merchant data
 */
function populateForm(merchant) {
    const form = document.querySelector('form');
    
    // Merchant name
    const nameInput = form.querySelector('input[name="name"]');
    if (nameInput) {
        nameInput.value = merchant.name;
    }
    
    // Location
    const locationInput = form.querySelector('input[name="location"]');
    if (locationInput) {
        locationInput.value = merchant.location || '';
    }
    
    // Notes
    const notesTextarea = form.querySelector('textarea[name="notes"]');
    if (notesTextarea) {
        notesTextarea.value = merchant.notes || '';
    }
    
    // Set up cancel button
    const cancelBtn = form.querySelector('.btn-outline');
    if (cancelBtn) {
        cancelBtn.href = `view.html?id=${merchant.id}`;
    }
    
    // Set up delete button
    const deleteBtn = form.querySelector('.btn-danger');
    if (deleteBtn) {
        deleteBtn.onclick = function() {
            deleteMerchantConfirm();
        };
    }
    
    // Add form submit listener
    form.addEventListener('submit', handleSubmit);
    
    // Add photo input listener
    const photoInput = document.getElementById('merchant-photo');
    if (photoInput) {
        photoInput.addEventListener('change', handlePhotoSelect);
    }
}

/**
 * Handle photo file selection
 */
function handlePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    selectedPhotoFile = file;
    
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
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    try {
        const form = document.querySelector('form');
        const nameInput = form.querySelector('input[name="name"]');
        const locationInput = form.querySelector('input[name="location"]');
        const notesTextarea = form.querySelector('textarea[name="notes"]');
        
        // Validation
        if (!nameInput.value) {
            alert('Merchant name is required');
            return;
        }
        
        if (!locationInput.value) {
            alert('Location is required');
            return;
        }
        
        const updateData = {
            name: nameInput.value,
            location: locationInput.value,
            notes: notesTextarea.value || null
        };
        
        await updateMerchant(currentMerchantId, updateData);
        
        // Upload photo if selected
        if (selectedPhotoFile) {
            await uploadMerchantPhoto(currentMerchantId, selectedPhotoFile);
        }
        
        alert('Merchant updated successfully!');
        window.location.href = `view.html?id=${currentMerchantId}`;
    } catch (error) {
        console.error('Error updating merchant:', error);
        alert('Error updating merchant: ' + error.message);
    }
}

/**
 * Delete merchant with confirmation
 */
async function deleteMerchantConfirm() {
    if (!confirm('Are you sure you want to delete this merchant?')) return;

    try {
        await deleteMerchant(currentMerchantId);
        alert('Merchant deleted successfully!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Error deleting merchant:', error);
        alert('Error deleting merchant: ' + error.message);
    }
}

// Expose to global scope
window.deleteMerchantConfirm = deleteMerchantConfirm;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchant();
});