/**
 * Merchant Detail - Spending Chart & Category Breakdown
 * Requires: Chart.js
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Include Chart.js before this script:
 *    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 * 2. Required HTML elements:
 *    - <canvas id="spendingChart"></canvas> (spending over time)
 *    - <canvas id="categoryChart"></canvas> (category breakdown)
 * 3. Replace sample data with merchant data from database
 * 
 * @requires Chart.js v3+
 */

/**
 * Spending Over Time Line Chart
 * Shows how much was spent at this merchant over time
 * 
 * REPLACE SAMPLE DATA with actual merchant spending history:
 * - Fetch merchant receipts grouped by date
 * - labels: Array of receipt dates
 * - data: Array of amounts spent on each date
 * 
 * @example
 * // Fetch from backend
 * fetch(`/api/merchants/${merchantId}/spending-history`)
 *   .then(res => res.json())
 *   .then(history => {
 *     spendingChart.data.labels = history.map(h => h.date);
 *     spendingChart.data.datasets[0].data = history.map(h => h.amount);
 *     spendingChart.update();
 *   });
 */
const spendingCtx = document.getElementById('spendingChart').getContext('2d');
const spendingChart = new Chart(spendingCtx, {
    type: 'line',
    data: {
        // REPLACE with actual dates from receipts
        labels: ['Sep 18', 'Oct 2', 'Oct 15', 'Oct 28', 'Nov 10'],
        datasets: [{
            label: 'Amount Spent (€)',
            // REPLACE with actual spending amounts
            data: [102.30, 68.50, 95.80, 42.15, 87.45],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            tension: 0.3,  // Smooth curve
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: '#2563eb',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return 'Spent: ' + context.parsed.y.toFixed(2) + ' €';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value.toFixed(2) + ' €';
                    }
                }
            }
        }
    }
});

/**
 * Category Breakdown Doughnut Chart
 * Shows which categories were purchased at this merchant
 * 
 * REPLACE SAMPLE DATA with actual category breakdown:
 * - Fetch products purchased at this merchant grouped by category
 * - labels: Array of category names
 * - data: Array of total spent per category
 * - backgroundColor: Array of category colors (from database)
 * 
 * @example
 * // Fetch from backend
 * fetch(`/api/merchants/${merchantId}/category-breakdown`)
 *   .then(res => res.json())
 *   .then(categories => {
 *     categoryChart.data.labels = categories.map(c => c.name);
 *     categoryChart.data.datasets[0].data = categories.map(c => c.total);
 *     categoryChart.data.datasets[0].backgroundColor = categories.map(c => c.color);
 *     categoryChart.update();
 *   });
 */
const categoryCtx = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(categoryCtx, {
    type: 'doughnut',
    data: {
        // REPLACE with actual category names
        labels: ['Dairy', 'Bakery', 'Meat', 'Vegetables', 'Fruits', 'Beverages', 'Other'],
        datasets: [{
            // REPLACE with actual spending per category
            data: [98.50, 145.30, 187.60, 92.40, 68.20, 75.40, 20.00],
            // REPLACE with category colors from database
            backgroundColor: [
                '#3b82f6',
                '#8b5cf6',
                '#ec4899',
                '#10b981',
                '#f59e0b',
                '#06b6d4',
                '#6b7280'
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    padding: 15,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return label + ': ' + value.toFixed(2) + ' € (' + percentage + '%)';
                    }
                }
            }
        }
    }
});
