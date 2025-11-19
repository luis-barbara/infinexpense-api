/**
 * Product Detail - Price History Chart & Photo Upload
 * Requires: Chart.js
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Include Chart.js before this script:
 *    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 * 2. Required HTML elements:
 *    - <canvas id="priceHistoryChart"></canvas>
 *    - <input type="file" id="photo-upload" accept="image/*">
 *    - <img id="product-image">
 *    - <div id="upload-area"></div>
 * 3. Replace sample data with historical price data from database
 * 
 * @requires Chart.js v3+
 */

/**
 * Initialize price history line chart
 * 
 * REPLACE SAMPLE DATA with actual price history from your backend:
 * - Fetch product price history from database
 * - labels: Array of dates (formatted strings)
 * - data: Array of prices at those dates
 * 
 * @example
 * // Fetch from backend
 * fetch(`/api/products/${productId}/price-history`)
 *   .then(res => res.json())
 *   .then(history => {
 *     priceHistoryChart.data.labels = history.map(h => h.date);
 *     priceHistoryChart.data.datasets[0].data = history.map(h => h.price);
 *     priceHistoryChart.update();
 *   });
 */
const ctx = document.getElementById('priceHistoryChart').getContext('2d');
const priceHistoryChart = new Chart(ctx, {
    type: 'line',
    data: {
        // REPLACE with actual dates from DB
        labels: ['Sep 5', 'Sep 20', 'Oct 1', 'Oct 15', 'Oct 28', 'Nov 10'],
        datasets: [{
            label: 'Price (€)',
            // REPLACE with actual price data from DB
            data: [0.85, 0.89, 0.92, 0.89, 0.85, 0.89],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            tension: 0,  // Straight lines (set to 0.3 for curves)
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
                        return 'Price: ' + context.parsed.y.toFixed(2) + ' €';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
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
 * Handle product photo upload
 * Allows user to select an image file and preview it
 * 
 * INTEGRATION:
 * - Upload image to server on change
 * - Store image URL in database
 * - Update product record with new image path
 * 
 * @listens change#photo-upload
 */
const photoUpload = document.getElementById('photo-upload');
const productImage = document.getElementById('product-image');
const uploadArea = document.getElementById('upload-area');

photoUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(event) {
            productImage.src = event.target.result;
            productImage.style.display = 'block';
            uploadArea.style.display = 'none';
            
            // INTEGRATION POINT: Upload to server
            // uploadImageToServer(file);
        };
        reader.readAsDataURL(file);
    }
});

/**
 * Click on image to change photo
 * Triggers file input when clicking the product image
 * 
 * @listens click#product-image
 */
productImage.addEventListener('click', function() {
    photoUpload.click();
});

/**
 * Example function for server upload
 * Uncomment and implement for actual backend integration
 * 
 * @param {File} file - The image file to upload
 * @example
 * async function uploadImageToServer(file) {
 *     const formData = new FormData();
 *     formData.append('photo', file);
 *     formData.append('product_id', productId);
 *     
 *     const response = await fetch('/api/products/upload-photo', {
 *         method: 'POST',
 *         body: formData
 *     });
 *     
 *     const result = await response.json();
 *     console.log('Image uploaded:', result.image_url);
 * }
 */
