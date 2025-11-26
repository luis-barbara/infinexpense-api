/**
 * Auto-include Dark Mode Toggle on all pages
 * This script automatically loads dark mode functionality on every page
 */

(function() {
    'use strict';
    
    // Function to load CSS file
    function loadCSS(href) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }
    
    // Function to load JavaScript file
    function loadJS(src, callback) {
        const script = document.createElement('script');
        script.src = src;
        script.onload = callback;
        document.head.appendChild(script);
    }
    
    // Detect the base path based on current location
    function getBasePath() {
        const currentPath = window.location.pathname;
        const depth = (currentPath.match(/\//g) || []).length - 1;
        
        if (depth === 0 || currentPath.endsWith('index.html')) {
            return './';
        } else {
            return '../'.repeat(depth - 1);
        }
    }
    
    // Initialize dark mode
    function initDarkMode() {
        const basePath = getBasePath();
        
        // Load dark mode CSS if not already loaded
        if (!document.querySelector('link[href*="dark-mode.css"]')) {
            loadCSS(`${basePath}/css/dark-mode.css`);
        }
        
        // Load and initialize dark mode JavaScript if not already loaded
        if (!document.querySelector('script[src*="dark-mode-toggle.js"]')) {
            loadJS(`${basePath}/js/dark-mode-toggle.js`);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDarkMode);
    } else {
        initDarkMode();
    }
})();