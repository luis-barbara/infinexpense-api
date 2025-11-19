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

        console.log('Loading merchant ID:', currentMerchantId);
        currentMerchant = await getMerchantById(currentMerchantId);
        console.log('Merchant loaded:', currentMerchant);

        // Update page title
        document.querySelector('.page-title').textContent = `Edit Merchant: ${currentMerchant.name}`;

        // Populate form
        populateForm(currentMerchant);
    } catch (error) {
        console.error('Erro ao carregar comerciante:', error);
        alert('Erro ao carregar comerciante: ' + error.message);
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
        console.log('Set merchant name to:', merchant.name);
    }
    
    // Location
    const locationInput = form.querySelector('input[name="location"]');
    if (locationInput) {
        locationInput.value = merchant.location || '';
        console.log('Set location to:', merchant.location);
    }
    
    // Notes
    const notesTextarea = form.querySelector('textarea[name="notes"]');
    if (notesTextarea) {
        notesTextarea.value = merchant.notes || '';
        console.log('Set notes to:', merchant.notes);
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
        
        console.log('Updating merchant:', updateData);
        await updateMerchant(currentMerchantId, updateData);
        
        // Upload photo if selected
        if (selectedPhotoFile) {
            await uploadMerchantPhoto(currentMerchantId, selectedPhotoFile);
        }
        
        alert('Comerciante atualizado com sucesso!');
        window.location.href = `view.html?id=${currentMerchantId}`;
    } catch (error) {
        console.error('Erro ao atualizar comerciante:', error);
        alert('Erro ao atualizar comerciante: ' + error.message);
    }
}

/**
 * Delete merchant with confirmation
 */
async function deleteMerchantConfirm() {
    if (!confirm('Tem a certeza que deseja eliminar este comerciante?')) return;

    try {
        await deleteMerchant(currentMerchantId);
        alert('Comerciante eliminado com sucesso!');
        window.location.href = 'list.html';
    } catch (error) {
        console.error('Erro ao eliminar comerciante:', error);
        alert('Erro ao eliminar comerciante: ' + error.message);
    }
}

// Expose to global scope
window.deleteMerchantConfirm = deleteMerchantConfirm;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchant();
});