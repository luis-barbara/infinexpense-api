import { createReceipt } from '../api/receipts_api.js';
import { getMerchants } from '../api/merchants_api.js';

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
});