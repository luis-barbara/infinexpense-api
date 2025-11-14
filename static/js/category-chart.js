/**
 * Categories Chart - Pie Chart Visualization
 * Requires: Chart.js and chartjs-plugin-datalabels
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Include Chart.js before this script:
 *    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 *    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
 * 2. Create canvas element: <canvas id="categoryChart"></canvas>
 * 3. Replace sample data with your backend data
 * 4. Match backgroundColor colors with category colors from database
 * 
 * DATA STRUCTURE:
 * - labels: Array of category names
 * - data: Array of spending amounts (numbers)
 * - backgroundColor: Array of hex colors matching each category
 * 
 * @requires Chart.js v3+
 * @requires chartjs-plugin-datalabels v2+
 */

/**
 * Initialize category spending pie chart
 * 
 * REPLACE SAMPLE DATA with actual data from your backend:
 * - Fetch categories from database with: name, total_spent, color
 * - Populate labels[], data[], and backgroundColor[] arrays
 * 
 * @example
 * // Fetch from backend
 * fetch('/api/categories/spending')
 *   .then(res => res.json())
 *   .then(categories => {
 *     const labels = categories.map(c => c.name);
 *     const data = categories.map(c => c.total_spent);
 *     const colors = categories.map(c => c.color);
 *     // Update chart data
 *   });
 */
const ctx = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(ctx, {
    type: 'pie',
    data: {
        // REPLACE these with data from your backend
        labels: [
            'Meat', 'Beverages', 'Dairy', 'Personal Care', 
            'Vegetables', 'Frozen', 'Fruits', 'Bakery', 
            'Cleaning', 'Snacks', 'Grains', 'Condiments'
        ],
        datasets: [{
            // REPLACE with actual spending data from DB
            data: [
                487.50, 312.45, 245.80, 267.80, 198.30, 178.90, 
                167.90, 156.40, 145.60, 134.20, 124.60, 89.70
            ],
            // REPLACE with category colors from DB
            backgroundColor: [
                '#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', 
                '#14b8a6', '#ec4899', '#f97316', '#06b6d4', '#6366f1',
                '#84cc16', '#a855f7'
            ],
            borderWidth: 2,
            borderColor: '#ffffff',
            hoverOffset: 20
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false  // Custom legend in HTML
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 12
                },
                padding: 12,
                displayColors: false,
                callbacks: {
                    title: function(context) {
                        return context[0].label;
                    },
                    label: function(context) {
                        const value = context.parsed.toFixed(2);
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                        return [percentage + '%', value + ' €'];
                    }
                }
            },
            datalabels: {
                color: '#ffffff',
                font: {
                    weight: 'bold',
                    size: 11
                },
                formatter: function(value, context) {
                    return context.chart.data.labels[context.dataIndex];
                },
                textAlign: 'center',
                anchor: 'center',
                align: 'center'
            }
        },
        animation: {
            animateRotate: true,
            animateScale: true
        }
    },
    plugins: [ChartDataLabels]
});
