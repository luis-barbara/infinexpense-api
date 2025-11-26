/**
 * Template Loader - Load Header and Footer Templates.
 */

(function() {
    'use strict';

    /**
     * Determine the base path based on current URL depth.
     */
    function getBasePath() {
        const path = window.location.pathname;
        
        if (path === '/' || path === '/index.html') {
            return '';
        }
        
        const depth = path.split('/').filter(p => p && p !== 'static').length - 1;
        return '../'.repeat(depth);
    }

    /**
     * Load a template file and inject it into the DOM
     * @param {HTMLElement} element - The element with data-template attribute
     * @param {string} templateName - Name of the template (header/footer)
     */
    async function loadTemplate(element, templateName) {
        try {
            // Always use /static/templates/ path since we're serving from root
            const response = await fetch(`/static/templates/${templateName}.html`);
            if (!response.ok) throw new Error(`Template ${templateName} not found`);
            
            let html = await response.text();
            
            // Inject the template
            element.innerHTML = html;
            
            // Set active navigation link if this is the header
            if (templateName === 'header') {
                setActiveNavLink();
            }
        } catch (error) {
            console.error(`Error loading template ${templateName}:`, error);
        }
    }

    /**
     * Set active class on navigation link based on current page.
     */
    function setActiveNavLink() {
        const activePage = document.body.getAttribute('data-active-page');
        if (!activePage) return;

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            if (link.getAttribute('data-page') === activePage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    /**
     * Load dark mode CSS and JS
     * @param {string} basePath - Base path for URLs
     */
    function loadDarkMode(basePath) {
        // Load dark mode CSS if not already loaded
        if (!document.querySelector('link[href*="dark-mode.css"]')) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = `${basePath}css/dark-mode.css`;
            document.head.appendChild(link);
        }
        
        // Load and initialize dark mode JavaScript if not already loaded
        if (!document.querySelector('script[src*="dark-mode-toggle.js"]')) {
            const script = document.createElement('script');
            script.src = `${basePath}js/dark-mode-toggle.js`;
            document.head.appendChild(script);
        }
    }

    /**
     * Initialize template loading on DOM ready
     */
    function init() {
        // Wait a tick to ensure DOM is fully parsed
        setTimeout(() => {
            const templateElements = document.querySelectorAll('[data-template]');
            
            if (templateElements.length > 0) {
                templateElements.forEach(element => {
                    const templateName = element.getAttribute('data-template');
                    loadTemplate(element, templateName);
                });
            }
            
            // Load theme script
            const themeScript = document.createElement('script');
            themeScript.src = '/static/js/theme.js';
            document.head.appendChild(themeScript);
        }, 0);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
