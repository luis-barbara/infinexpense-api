// static/js/receipts.js
const API_URL = 'http://localhost:8000/receipts';

// Carregar todos os recibos
async function loadReceipts() {
    try {
        const response = await fetch(API_URL);
        const receipts = await response.json();
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

    if (receipts.length === 0) {
        container.innerHTML = '<p>Nenhum recibo encontrado</p>';
        return;
    }

    receipts.forEach(receipt => {
        const receiptCard = document.createElement('div');
        receiptCard.className = 'receipt-card';
        receiptCard.innerHTML = `
            <h3>Recibo #${receipt.id}</h3>
            <p><strong>Comerciante:</strong> ${receipt.merchant_id}</p>
            <p><strong>Data:</strong> ${new Date(receipt.date).toLocaleDateString('pt-PT')}</p>
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

// Criar novo recibo
document.getElementById('receiptForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const receiptData = {
        merchant_id: parseInt(document.getElementById('merchantId').value),
        date: document.getElementById('receiptDate').value,
        barcode: document.getElementById('barcode').value || null,
        products: [] // Pode adicionar produtos depois
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(receiptData)
        });

        if (response.ok) {
            alert('Recibo criado com sucesso!');
            document.getElementById('receiptForm').reset();
            loadReceipts();
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error('Erro ao criar recibo:', error);
        alert('Erro ao criar recibo');
    }
});

// Filtrar recibos
async function filterReceipts() {
    const merchantId = document.getElementById('filterMerchant').value;
    const startDate = document.getElementById('filterStartDate').value;
    const endDate = document.getElementById('filterEndDate').value;

    let url = `${API_URL}?`;
    const params = [];

    if (merchantId) params.push(`merchant_id=${merchantId}`);
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);

    url += params.join('&');

    try {
        const response = await fetch(url);
        const receipts = await response.json();
        displayReceipts(receipts);
    } catch (error) {
        console.error('Erro ao filtrar recibos:', error);
        alert('Erro ao filtrar recibos');
    }
}

// Ver detalhes do recibo
async function viewReceipt(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        const receipt = await response.json();
        
        // Mostrar modal ou navegar para página de detalhes
        alert(JSON.stringify(receipt, null, 2));
    } catch (error) {
        console.error('Erro ao carregar recibo:', error);
    }
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
        }
    } catch (error) {
        console.error('Erro ao eliminar recibo:', error);
        alert('Erro ao eliminar recibo');
    }
}

// Carregar recibos ao iniciar a página
document.addEventListener('DOMContentLoaded', loadReceipts);