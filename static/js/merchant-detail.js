/**
 * Merchant Detail - Spending Chart
 * Requires: Chart.js
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Include Chart.js before this script:
 *    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 * 2. Required HTML elements:
 *    - <canvas id="merchantSpendingChart"></canvas> (spending over time)
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
 *     merchantSpendingChart.data.labels = history.map(h => h.date);
 *     merchantSpendingChart.data.datasets[0].data = history.map(h => h.amount);
 *     merchantSpendingChart.update();
 *   });
 */
const merchantSpendingCtx = document.getElementById('merchantSpendingChart');
if (merchantSpendingCtx) {
    const merchantSpendingChart = new Chart(merchantSpendingCtx.getContext('2d'), {
        type: 'bar',
        data: {
            // REPLACE with actual dates from receipts
            labels: ['Sep 18', 'Oct 2', 'Oct 15', 'Oct 28', 'Nov 10'],
            datasets: [{
                label: 'Amount Spent (€)',
                // REPLACE with actual spending amounts
                data: [102.30, 68.50, 95.80, 42.15, 87.45],
                backgroundColor: '#2563eb',
                borderColor: '#2563eb',
                borderWidth: 0,
                borderRadius: 6,
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
}
