import { createMerchant } from '/static/api/merchants_api.js';

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
        
        alert('Comerciante criado com sucesso!');
        window.location.href = `/static/merchant/view.html?id=${createdMerchant.id}`;
    } catch (error) {
        console.error('Error creating merchant:', error);
        alert('Error creating merchant: ' + error.message);
    }
}

// Initialize on page load
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
