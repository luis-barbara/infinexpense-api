import { createReceipt } from '../api/receipts_api.js';
import { getMerchants } from '../api/merchants_api.js';
import { uploadReceiptPhoto } from '../api/uploads_api.js';

let selectedPhotoFile = null;

/**
 * Load merchants for dropdown
 */
async function loadMerchants() {
    try {
        const merchants = await getMerchants();
        const select = document.getElementById('merchantSelect');
        
        merchants.forEach(merchant => {
            const option = document.createElement('option');
            option.value = merchant.id;
            option.textContent = merchant.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading merchants:', error);
        alert('Error loading merchants: ' + error.message);
    }
}

/**
 * Set today's date as default
 */
function setDefaultDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('receiptDate').value = today;
}

/**
 * Handle photo file selection
 */
function handlePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    selectedPhotoFile = file;
    
    // Show preview in the upload label
    const label = document.querySelector('label[for="receiptPhoto"]');
    if (label) {
        const reader = new FileReader();
        reader.onload = function(event) {
            label.innerHTML = `<img src="${event.target.result}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">`;
        };
        reader.readAsDataURL(file);
    }
}

/**
 * Upload photo to server
 */
async function uploadPhoto(receiptId) {
    if (!selectedPhotoFile) return null;
    try {
        await uploadReceiptPhoto(receiptId, selectedPhotoFile);
        return true;
    } catch (error) {
        console.error('Error uploading photo:', error);
        return false;
    }
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    const merchantId = parseInt(document.getElementById('merchantSelect').value);
    const date = document.getElementById('receiptDate').value;
    const code = document.getElementById('receiptCode').value;
    const notes = document.getElementById('receiptNotes').value;
    if (!merchantId || !date) {
        alert('Please fill in all required fields');
        return;
    }
    try {
        const receiptData = {
            merchant_id: merchantId,
            purchase_date: date,
            barcode: code || null,
            notes: notes || null
        };
        const newReceipt = await createReceipt(receiptData);
        // Upload photo if selected
        if (selectedPhotoFile) {
            await uploadPhoto(newReceipt.id);
        }
        alert('Receipt created successfully!');
        window.location.href = `view.html?id=${newReceipt.id}`;
    } catch (error) {
        console.error('Error creating receipt:', error);
        alert('Error creating receipt: ' + error.message);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMerchants();
    setDefaultDate();
    const form = document.getElementById('addReceiptForm');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    // Handle photo input
    const photoInput = document.getElementById('receiptPhoto');
    if (photoInput) {
        photoInput.addEventListener('change', handlePhotoSelect);
    }
});