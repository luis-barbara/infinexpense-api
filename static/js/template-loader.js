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
     * Load a template file and inject it into the DOM.
     */
    async function loadTemplate(element, templateName, basePath) {
        try {
            const templatePath = basePath === '' ? `/templates/${templateName}.html` : `${basePath}templates/${templateName}.html`;
            
            const response = await fetch(templatePath);
            if (!response.ok) throw new Error(`Template ${templateName} not found at ${templatePath}`);
            
            let html = await response.text();
            
            // Replace {BASE_PATH} placeholder with actual base path
            const replacementPath = basePath === '' ? '/' : basePath;
            html = html.replace(/{BASE_PATH}/g, replacementPath);
            console.log('Replaced BASE_PATH with:', replacementPath);
            
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
     * Initialize template loading on DOM ready.
     */
    function init() {
        const basePath = getBasePath();
        const templateElements = document.querySelectorAll('[data-template]');
        
        templateElements.forEach(element => {
            const templateName = element.getAttribute('data-template');
            loadTemplate(element, templateName, basePath);
        });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
