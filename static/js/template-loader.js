/**
 * Template Loader - Load Header and Footer Templates
 * 
 * USAGE:
 * 1. Add data-template attribute to placeholder divs
 * 2. Add data-active-page attribute to body element
 * 3. Script will automatically load and inject templates
 * 
 * @example
 * <body data-active-page="dashboard">
 *     <div data-template="header"></div>
 *     <!-- Your page content -->
 *     <div data-template="footer"></div>
 * </body>
 */

(function() {
    'use strict';

    /**
     * Determine the base path based on current URL depth
     * @returns {string} Base path (e.g., '', '../', '../../')
     */
    function getBasePath() {
        const path = window.location.pathname;
        console.log('Current path:', path); // Debug log
        
        // If we're at root (/) or /index.html, use empty base path
        if (path === '/' || path === '/index.html') {
            return '';
        }
        
        // For other paths, calculate depth
        const depth = path.split('/').filter(p => p && p !== 'static').length - 1;
        return '../'.repeat(depth);
    }

    /**
     * Load a template file and inject it into the DOM
     * @param {HTMLElement} element - The element with data-template attribute
     * @param {string} templateName - Name of the template (header/footer)
     * @param {string} basePath - Base path for URLs
     */
    async function loadTemplate(element, templateName, basePath) {
        try {
            const templatePath = basePath === '' ? `/templates/${templateName}.html` : `${basePath}templates/${templateName}.html`;
            console.log('Loading template from:', templatePath); // Debug log
            
            const response = await fetch(templatePath);
            if (!response.ok) throw new Error(`Template ${templateName} not found at ${templatePath}`);
            
            let html = await response.text();
            
            // Replace {BASE_PATH} placeholder with actual base path
            const replacementPath = basePath === '' ? '/' : basePath;
            html = html.replace(/{BASE_PATH}/g, replacementPath);
            console.log('Replaced BASE_PATH with:', replacementPath); // Debug log
            
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
     * Set active class on navigation link based on current page
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
     * Initialize template loading on DOM ready
     */
    function init() {
        const basePath = getBasePath();
        const templateElements = document.querySelectorAll('[data-template]');
        
        templateElements.forEach(element => {
            const templateName = element.getAttribute('data-template');
            loadTemplate(element, templateName, basePath);
        });
    }

    // Run initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
