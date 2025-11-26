import { getReceipts } from '../api/receipts_api.js';

/**
 * Dashboard - Expense Comparison Toggle
 */

let showPercentage = true;
let autoSwitchInterval = null;

/**
 * Toggle between percentage and absolute value display
 */
function toggleComparisonMode() {
    showPercentage = !showPercentage;
    updateComparisonDisplay();
}

/**
 * Start auto-switching between % and €
 */
function startAutoSwitch() {
    if (autoSwitchInterval) clearInterval(autoSwitchInterval);
    autoSwitchInterval = setInterval(() => {
        showPercentage = !showPercentage;
        updateComparisonDisplay();
    }, 5000);
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
        comparisonEl.className = `stat-counter ${percentage > 0 ? 'stat-counter-negative' : 'stat-counter-positive'}`;
    } else {
        comparisonEl.textContent = `${difference > 0 ? '+' : ''}${difference.toFixed(2)} €`;
        comparisonEl.className = `stat-counter ${difference > 0 ? 'stat-counter-negative' : 'stat-counter-positive'}`;
    }
}

/**
 * Load recent receipts for dashboard
 */
async function loadRecentReceipts() {
    try {
        const receipts = await getReceipts({ skip: 0, limit: 100 });
        // Sort by creation date descending (newest first)
        receipts.sort((a, b) => new Date(b.created_at || b.purchase_date) - new Date(a.created_at || a.purchase_date));
        renderRecentReceipts(receipts.slice(0, 3));
    } catch (error) {
        console.error('Error loading recent receipts:', error);
    }
}

/**
 * Render recent receipts to dashboard
 */
function renderRecentReceipts(receipts) {
    const container = document.getElementById('recent-receipts-list');
    if (!container) return;

    container.innerHTML = '';

    if (receipts.length === 0) {
        container.innerHTML = '<div style="padding: 2rem; text-align: center; color: hsl(var(--muted-foreground));">No receipts found. <a href="receipts/add.html">Create one</a></div>';
        return;
    }

    receipts.forEach(receipt => {
        const receiptDate = new Date(receipt.purchase_date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });

        const card = document.createElement('a');
        card.href = `/static/receipt/view.html?id=${receipt.id}`;
        card.className = 'card glow-strong block';
        card.style.cssText = 'text-decoration: none; transition: all 0.2s ease;';
        card.setAttribute('data-receipt-id', receipt.id);
        card.setAttribute('onmouseover', "this.style.transform='translateY(-2px)'");
        card.setAttribute('onmouseout', "this.style.transform='translateY(0)'");

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <h3 style="font-size: 1.125rem; font-weight: 700; color: hsl(var(--foreground)); margin-bottom: 0.25rem;">${receipt.merchant?.name || 'Unknown Merchant'}</h3>
                    <p style="font-size: 0.75rem; color: hsl(var(--muted-foreground)); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">PRODUCTS</p>
                    <p style="font-size: 0.875rem; color: hsl(var(--muted-foreground));">${receipt.products?.length || 0} items</p>
                </div>
                <div style="text-align: right;">
                    <p style="font-size: 0.875rem; color: hsl(var(--muted-foreground)); margin-bottom: 0.5rem;">${receiptDate}</p>
                    <p style="font-size: 1.5rem; font-weight: 700; color: hsl(var(--primary));">${parseFloat(receipt.total_price || 0).toFixed(2)} €</p>
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
            receiptsComparisonEl.className = `stat-counter ${receiptsDifference > 0 ? 'stat-counter-negative' : 'stat-counter-positive'}`;
        }

        // Update UI - Products Purchased
        const productsEl = document.getElementById('products-purchased');
        if (productsEl) {
            productsEl.textContent = currentProducts;
        }

        const productsComparisonEl = document.getElementById('products-comparison');
        if (productsComparisonEl) {
            productsComparisonEl.textContent = `${productsDifference > 0 ? '+' : ''}${productsDifference} from last month`;
            productsComparisonEl.className = `stat-counter ${productsDifference > 0 ? 'stat-counter-negative' : 'stat-counter-positive'}`;
        }

        // Update comparison display for expenses
        const comparisonEl = document.getElementById('expense-comparison');
        if (comparisonEl) {
            comparisonEl.setAttribute('data-current-expense', currentExpenses);
            comparisonEl.setAttribute('data-last-month-expense', lastMonthExpenses);
            updateComparisonDisplay();
            comparisonEl.style.cursor = 'pointer';
            comparisonEl.onclick = function(e) {
                e.stopPropagation();
                showPercentage = !showPercentage;
                updateComparisonDisplay();
            };
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Expose to global scope
window.toggleComparisonMode = toggleComparisonMode;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRecentReceipts();
    loadDashboardStats();
    startAutoSwitch();
});
