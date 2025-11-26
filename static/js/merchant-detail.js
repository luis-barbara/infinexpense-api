/**
 * Merchant Detail Page - Display merchant spending chart.
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
