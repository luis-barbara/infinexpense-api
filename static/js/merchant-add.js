import { createMerchant, uploadMerchantPhoto } from '../api/merchants_api.js';

let selectedPhotoFile = null;

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
        
        console.log('Form inputs:', {
            nameInput: nameInput?.value,
            locationInput: locationInput?.value,
            notesTextarea: notesTextarea?.value
        });
        
        // Validation
        if (!nameInput || !nameInput.value) {
            alert('Merchant name is required');
            return;
        }
        
        if (!locationInput || !locationInput.value) {
            alert('Location is required');
            return;
        }
        
        const newMerchant = {
            name: nameInput.value,
            location: locationInput.value,
            notes: notesTextarea?.value || null
        };
        
        console.log('Creating merchant:', newMerchant);
        const createdMerchant = await createMerchant(newMerchant);
        console.log('Merchant created:', createdMerchant);
        
        // Upload photo if selected
        if (selectedPhotoFile) {
            await uploadMerchantPhoto(createdMerchant.id, selectedPhotoFile);
        }
        
        alert('Comerciante criado com sucesso!');
        window.location.href = `view.html?id=${createdMerchant.id}`;
    } catch (error) {
        console.error('Erro ao criar comerciante:', error);
        alert('Erro ao criar comerciante: ' + error.message);
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
    console.log('Merchant add page loaded');
    
    const form = document.querySelector('form');
    if (form) {
        console.log('Form found, adding submit listener');
        form.addEventListener('submit', handleSubmit);
    } else {
        console.warn('Form not found');
    }
    
    // Handle photo input
    const photoInput = document.getElementById('merchant-photo');
    if (photoInput) {
        console.log('Photo input found');
        photoInput.addEventListener('change', handlePhotoSelect);
    }
});