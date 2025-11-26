import { createMerchant, uploadMerchantPhoto } from '../api/merchants_api.js';

let selectedPhotoFile = null;

/**
 * Handle photo file selection.
 */
function handlePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    selectedPhotoFile = file;
    
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
 * Handle form submission.
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    try {
        const form = document.querySelector('form');
        const nameInput = form.querySelector('input[name="name"]');
        const locationInput = form.querySelector('input[name="location"]');
        const notesTextarea = form.querySelector('textarea[name="notes"]');
        
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
        
        if (selectedPhotoFile) {
            await uploadMerchantPhoto(createdMerchant.id, selectedPhotoFile);
        }
        
        alert('Merchant created successfully!');
        window.location.href = `view.html?id=${createdMerchant.id}`;
    } catch (error) {
        console.error('Error creating merchant:', error);
        alert('Error creating merchant: ' + error.message);
    }
}

/**
 * Cancel add.
 */
function cancelAdd() {
    window.location.href = 'list.html';
}

window.cancelAdd = cancelAdd;
window.handlePhotoSelect = handlePhotoSelect;

document.addEventListener('DOMContentLoaded', async function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    const photoInput = document.getElementById('merchant-photo');
    if (photoInput) {
        photoInput.addEventListener('change', handlePhotoSelect);
    }
});
