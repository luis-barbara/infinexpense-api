/**
 * Dashboard - Expense Comparison Toggle
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Populate lastMonthExpense and currentExpense from your backend/database
 * 2. The toggle function switches between percentage and absolute value display
 * 3. Bind this to the element with id="expenseComparison"
 * 
 * DATA BINDING:
 * - Element: document.getElementById('expenseComparison')
 * - Can use data-field="expense-comparison" for backend integration
 */

// REPLACE THESE VALUES with data from your backend
let showPercentage = true;
const lastMonthExpense = 2533.13; // Previous month total - fetch from DB
const currentExpense = 2847.65;    // Current month total - fetch from DB
const difference = currentExpense - lastMonthExpense;
const percentage = ((difference / lastMonthExpense) * 100).toFixed(1);

/**
 * Toggle between percentage and absolute value display
 * 
 * Shows either:
 * - "+12.5% from last month" (percentage mode)
 * - "+314.52 € from last month" (absolute value mode)
 * 
 * @example
 * // In HTML: <span id="expenseComparison" onclick="toggleComparisonMode()">+12.5% from last month</span>
 */
function toggleComparisonMode() {
    const element = document.getElementById('expenseComparison');
    showPercentage = !showPercentage;
    
    if (showPercentage) {
        element.textContent = `+${percentage}% from last month`;
    } else {
        element.textContent = `+${difference.toFixed(2)} € from last month`;
    }
}
