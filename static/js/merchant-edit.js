import { getMerchantById, updateMerchant, deleteMerchant } from '/static/api/merchants_api.js';

let currentMerchantId = null;
let currentMerchant = null;

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
            window.location.href = '/static/merchant/list.html';
            return;
        }

        console.log('Loading merchant ID:', currentMerchantId);
        currentMerchant = await getMerchantById(currentMerchantId);
        console.log('Merchant loaded:', currentMerchant);

        // Update page title
        const titleEl = document.querySelector('h1.gradient-text');
        if (titleEl) {
            titleEl.textContent = `Edit Merchant: ${currentMerchant.name}`;
        }

        // Populate form
        populateForm(currentMerchant);
    } catch (error) {
        console.error('Erro ao carregar comerciante:', error);
        alert('Erro ao carregar comerciante: ' + error.message);
        window.location.href = '/static/merchant/list.html';
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
    const cancelBtn = form.querySelector('a[href*="list.html"]');
    if (cancelBtn) {
        cancelBtn.href = `/static/merchant/list.html`;
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
        
        alert('Comerciante atualizado com sucesso!');
        window.location.href = `/static/merchant/view.html?id=${currentMerchantId}`;
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
        window.location.href = '/static/merchant/list.html';
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