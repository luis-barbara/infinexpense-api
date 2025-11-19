// static/js/receipts.js  (v3-debug)
const API_URL = 'http://localhost:8000/receipts';


// --------- Helpers ---------

function formatReceiptDate(purchase_date) {
    if (!purchase_date) return 'N/A';
    const isoPart = String(purchase_date).split('T')[0];
    const parts = isoPart.split('-');

    if (parts.length !== 3) {
        return String(purchase_date);
    }

    const [year, month, day] = parts;
    if (!year || !month || !day) {
        return String(purchase_date);
    }

    return `${day}/${month}/${year}`;
}

// --------- Load & display receipts ---------

// Carregar todos os recibos
async function loadReceipts() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const receipts = await response.json();
        console.log('Receipts carregados:', receipts);
        displayReceipts(receipts);
    } catch (error) {
        console.error('Erro ao carregar recibos:', error);
        alert('Erro ao carregar recibos');
    }
}

// Exibir recibos na página
function displayReceipts(receipts) {
    const container = document.getElementById('receiptsContainer');
    container.innerHTML = '';

    if (!receipts || receipts.length === 0) {
        container.innerHTML = '<p>Nenhum recibo encontrado</p>';
        return;
    }

    receipts.forEach((receipt) => {
        const receiptCard = document.createElement('div');
        receiptCard.className = 'receipt-card';

        const merchantName =
            (receipt.merchant && receipt.merchant.name) || receipt.merchant_id || 'N/A';

        const formattedDate = formatReceiptDate(receipt.purchase_date);

        receiptCard.innerHTML = `
            <h3>Recibo #${receipt.id}</h3>
            <p><strong>Merchant:</strong> ${merchantName}</p>
            <p><strong>Data:</strong> ${formattedDate}</p>
            <p><strong>Código de Barras:</strong> ${receipt.barcode || 'N/A'}</p>
            <div class="actions">
                <button onclick="viewReceipt(${receipt.id})">Ver Detalhes</button>
                <button onclick="editReceipt(${receipt.id})">Editar</button>
                <button onclick="deleteReceipt(${receipt.id})" class="delete-btn">Eliminar</button>
            </div>
        `;
        container.appendChild(receiptCard);
    });
}

// --------- Create receipt ---------

// Criar novo recibo
document.getElementById('receiptForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const merchantIdValue = document.getElementById('merchantId').value;
    const purchaseDateValue = document.getElementById('receiptDate').value;
    const barcodeValue = document.getElementById('barcode').value;

    if (!merchantIdValue) {
        alert('Por favor, indique o ID do comerciante.');
        return;
    }

    if (!purchaseDateValue) {
        alert('Por favor, selecione uma data para o recibo.');
        return;
    }

    const receiptData = {
        merchant_id: parseInt(merchantIdValue, 10),
        purchase_date: purchaseDateValue, // "YYYY-MM-DD" vindo do <input type="date">
        barcode: barcodeValue || null,
        products: [] // Pode adicionar produtos depois
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(receiptData)
        });

        if (response.ok) {
            alert('Recibo criado com sucesso!');
            document.getElementById('receiptForm').reset();
            loadReceipts();
        } else {
            let errorMsg = `Erro HTTP ${response.status}`;
            try {
                const error = await response.json();
                if (error && error.detail) {
                    errorMsg = `Erro: ${error.detail}`;
                }
            } catch (_) {
                // ignore JSON parse error
            }
            alert(errorMsg);
        }
    } catch (error) {
        console.error('Erro ao criar recibo:', error);
        alert('Erro ao criar recibo');
    }
});

// --------- Filter receipts ---------

// Filtrar recibos
async function filterReceipts() {
    const merchantId = document.getElementById('filterMerchant').value;
    const startDate = document.getElementById('filterStartDate').value;
    const endDate = document.getElementById('filterEndDate').value;

    const params = [];

    if (merchantId) params.push(`merchant_id=${encodeURIComponent(merchantId)}`);
    if (startDate) params.push(`start_date=${encodeURIComponent(startDate)}`);
    if (endDate) params.push(`end_date=${encodeURIComponent(endDate)}`);

    const url = params.length ? `${API_URL}?${params.join('&')}` : API_URL;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const receipts = await response.json();
        console.log('Receipts filtrados:', receipts);
        displayReceipts(receipts);
    } catch (error) {
        console.error('Erro ao filtrar recibos:', error);
        alert('Erro ao filtrar recibos');
    }
}

// --------- View / Edit / Delete ---------

// Ver detalhes do recibo
async function viewReceipt(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const receipt = await response.json();
        alert(JSON.stringify(receipt, null, 2));
    } catch (error) {
        console.error('Erro ao carregar recibo:', error);
        alert('Erro ao carregar detalhes do recibo');
    }
}

function editReceipt(id) {
    alert(`Funcionalidade de edição ainda não implementada (ID: ${id})`);
}

// Eliminar recibo
async function deleteReceipt(id) {
    if (!confirm('Tem a certeza que deseja eliminar este recibo?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Recibo eliminado com sucesso!');
            loadReceipts();
        } else {
            alert(`Erro ao eliminar recibo (HTTP ${response.status})`);
        }
    } catch (error) {
        console.error('Erro ao eliminar recibo:', error);
        alert('Erro ao eliminar recibo');
    }
}

// --------- Init ---------

// Carregar recibos ao iniciar a página
document.addEventListener('DOMContentLoaded', loadReceipts);
