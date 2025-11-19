import { getReceipts } from '../api/receipts_api.js';

/**
 * Dashboard - Expense Comparison Toggle
 */

let showPercentage = true;

/**
 * Toggle between percentage and absolute value display
 */
function toggleComparisonMode() {
    showPercentage = !showPercentage;
    updateComparisonDisplay();
}

function updateComparisonDisplay() {
    const comparisonEl = document.getElementById('expense-comparison');
    if (!comparisonEl) return;

    const currentExpense = parseFloat(comparisonEl.getAttribute('data-current-expense')) || 0;
    const lastMonthExpense = parseFloat(comparisonEl.getAttribute('data-last-month-expense')) || 0;
    const difference = currentExpense - lastMonthExpense;
    const percentage = lastMonthExpense > 0 ? ((difference / lastMonthExpense) * 100).toFixed(1) : 0;

    if (showPercentage) {
        comparisonEl.textContent = `${percentage > 0 ? '+' : ''}${percentage}%`;
        comparisonEl.className = percentage > 0 ? 'comparison-negative' : 'comparison-positive';
    } else {
        comparisonEl.textContent = `${difference > 0 ? '+' : ''}${difference.toFixed(2)} €`;
        comparisonEl.className = difference > 0 ? 'comparison-negative' : 'comparison-positive';
    }
}

/**
 * Load recent receipts for dashboard
 */
async function loadRecentReceipts() {
    try {
        const receipts = await getReceipts({ skip: 0, limit: 3 });
        renderRecentReceipts(receipts);
    } catch (error) {
        console.error('Erro ao carregar recibos recentes:', error);
    }
}

/**
 * Render recent receipts to dashboard
 */
function renderRecentReceipts(receipts) {
    const container = document.getElementById('recent-receipts-list');
    if (!container) return;

    container.innerHTML = '';

    receipts.forEach(receipt => {
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('pt-PT', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        const card = document.createElement('a');
        card.href = `receipt/view.html?id=${receipt.id}`;
        card.className = 'receipt-card';
        card.setAttribute('data-receipt-id', receipt.id);

        card.innerHTML = `
            <div class="receipt-header">
                <div>
                    <div class="receipt-merchant">${receipt.merchant?.name || 'Unknown Merchant'}</div>
                    <div class="receipt-detail-item" style="margin-top: 0.5rem;">
                        <span class="receipt-detail-label">Products</span>
                        <span class="receipt-detail-value">${receipt.products?.length || 0} items</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div class="receipt-date">${receiptDate}</div>
                    <div class="receipt-detail-value" style="margin-top: 0.5rem; font-size: 1.5rem; color: var(--primary-color);">
                        ${parseFloat(receipt.total_price || 0).toFixed(2)} €
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

/**
 * Load statistics from receipts
 */
async function loadDashboardStats() {
    try {
        const receipts = await getReceipts({ limit: 1000 });

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth();
        const currentYear = now.getFullYear();

        // Get last month
        const lastMonth = currentMonth === 0 ? 11 : currentMonth - 1;
        const lastMonthYear = currentMonth === 0 ? currentYear - 1 : currentYear;

        // Filter receipts for current month
        const currentMonthReceipts = receipts.filter(r => {
            const receiptDate = new Date(r.purchase_date);
            return receiptDate.getMonth() === currentMonth && 
                   receiptDate.getFullYear() === currentYear;
        });

        // Filter receipts for last month
        const lastMonthReceipts = receipts.filter(r => {
            const receiptDate = new Date(r.purchase_date);
            return receiptDate.getMonth() === lastMonth && 
                   receiptDate.getFullYear() === lastMonthYear;
        });

        // Calculate statistics
        const currentExpenses = currentMonthReceipts.reduce((sum, r) => sum + parseFloat(r.total_price || 0), 0);
        const lastMonthExpenses = lastMonthReceipts.reduce((sum, r) => sum + parseFloat(r.total_price || 0), 0);
        const currentProducts = currentMonthReceipts.reduce((sum, r) => sum + (r.products?.length || 0), 0);
        const lastMonthProducts = lastMonthReceipts.reduce((sum, r) => sum + (r.products?.length || 0), 0);

        const receiptsDifference = currentMonthReceipts.length - lastMonthReceipts.length;
        const productsDifference = currentProducts - lastMonthProducts;

        // Update UI - Monthly Expenses
        const monthlyExpensesEl = document.getElementById('monthly-expenses');
        if (monthlyExpensesEl) {
            monthlyExpensesEl.textContent = `${currentExpenses.toFixed(2)} €`;
        }

        // Update UI - Total Receipts
        const totalReceiptsEl = document.getElementById('total-receipts');
        if (totalReceiptsEl) {
            totalReceiptsEl.textContent = currentMonthReceipts.length;
        }

        const receiptsComparisonEl = document.getElementById('receipts-comparison');
        if (receiptsComparisonEl) {
            receiptsComparisonEl.textContent = `${receiptsDifference > 0 ? '+' : ''}${receiptsDifference} from last month`;
            receiptsComparisonEl.className = receiptsDifference > 0 ? 'comparison-positive' : 'comparison-negative';
        }

        // Update UI - Products Purchased
        const productsEl = document.getElementById('products-purchased');
        if (productsEl) {
            productsEl.textContent = currentProducts;
        }

        const productsComparisonEl = document.getElementById('products-comparison');
        if (productsComparisonEl) {
            productsComparisonEl.textContent = `${productsDifference > 0 ? '+' : ''}${productsDifference} from last month`;
            productsComparisonEl.className = productsDifference > 0 ? 'comparison-positive' : 'comparison-negative';
        }

        // Update comparison display for expenses
        const comparisonEl = document.getElementById('expense-comparison');
        if (comparisonEl) {
            comparisonEl.setAttribute('data-current-expense', currentExpenses);
            comparisonEl.setAttribute('data-last-month-expense', lastMonthExpenses);
            updateComparisonDisplay();
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Expose to global scope
window.toggleComparisonMode = toggleComparisonMode;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRecentReceipts();
    loadDashboardStats();
});
