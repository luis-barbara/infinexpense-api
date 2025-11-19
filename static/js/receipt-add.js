import { createReceipt } from '../api/receipts_api.js';
import { getMerchants } from '../api/merchants_api.js';

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
        console.error('Erro ao carregar comerciantes:', error);
        alert('Erro ao carregar comerciantes: ' + error.message);
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
async function uploadPhoto(receiptId) {
    if (!selectedPhotoFile) return null;
    try {
        const formData = new FormData();
        formData.append('file', selectedPhotoFile);
        const response = await fetch(`http://localhost:8000/receipts/${receiptId}/upload-photo`, {
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
    const merchantId = parseInt(document.getElementById('merchantSelect').value);
    const date = document.getElementById('receiptDate').value;
    const code = document.getElementById('receiptCode').value;
    const notes = document.getElementById('receiptNotes').value;
    if (!merchantId || !date) {
        alert('Preencha todos os campos obrigatórios');
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
        alert('Recibo criado com sucesso!');
        window.location.href = `view.html?id=${newReceipt.id}`;
    } catch (error) {
        console.error('Erro ao criar recibo:', error);
        alert('Erro ao criar recibo: ' + error.message);
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
    const photoInput = document.getElementById('receipt-photo');
    if (photoInput) {
        photoInput.addEventListener('change', handlePhotoSelect);
    }
});