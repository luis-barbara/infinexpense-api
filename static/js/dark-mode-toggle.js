/**
 * Dark Mode Toggle Functionality
 * Manages theme switching between light and dark modes
 */

class DarkModeToggle {
    constructor() {
        this.storageKey = 'infinexpense-theme';
        this.darkModeClass = 'dark-mode';
        this.init();
    }

    init() {
        this.createToggleButton();
        this.loadSavedTheme();
        this.bindEvents();
    }

    createToggleButton() {
        // Create the toggle button HTML with your specific SVG icons
        const toggleButton = document.createElement('button');
        toggleButton.id = 'theme-toggle';
        toggleButton.className = 'theme-toggle';
        toggleButton.setAttribute('aria-label', 'Toggle dark mode');
        
        // Sun SVG (light.svg - shown in dark mode to switch to light)
        const sunSVG = `
            <svg class="theme-toggle-icon sun-icon" viewBox="0 0 512 512" width="32" height="32" fill="currentColor">
                <path fill="#F9AA45" d="M498.526,256.001l-73.297,54.973l26.947,87.633l-91.621,1.293l-29.642,86.771L256,433.853
                    l-74.914,52.817l-29.642-86.771l-91.621-1.293l26.947-87.633l-73.297-54.973l73.297-54.973l-26.947-87.633l91.621-1.293
                    l29.642-86.771L256,78.148l74.914-52.817l29.642,86.771l91.621,1.293l-26.947,87.633L498.526,256.001z M385.347,256.001
                    c0-71.464-57.883-129.347-129.347-129.347s-129.347,57.883-129.347,129.347S184.536,385.348,256,385.348
                    S385.347,327.465,385.347,256.001z"/>
                <path fill="#FFD248" d="M256,126.653c71.464,0,129.347,57.883,129.347,129.347S327.464,385.348,256,385.348
                    s-129.347-57.883-129.347-129.347S184.536,126.653,256,126.653z"/>
            </svg>
        `;
        
        // Moon SVG (night.svg - shown in light mode to switch to dark)
        const moonSVG = `
            <svg class="theme-toggle-icon moon-icon" viewBox="0 0 512 512" width="32" height="32" fill="currentColor">
                <circle fill="#77AAD4" cx="256.003" cy="256.003" r="248"/>
                <g>
                    <circle fill="#1D71B8" cx="288.003" cy="64.001" r="23.998"/>
                    <circle fill="#1D71B8" cx="175.997" cy="256.003" r="16"/>
                    <circle fill="#1D71B8" cx="64.001" cy="376.001" r="16"/>
                    <circle fill="#1D71B8" cx="335.998" cy="175.997" r="16"/>
                    <circle fill="#1D71B8" cx="200.005" cy="440.002" r="23.998"/>
                    <circle fill="#1D71B8" cx="79.996" cy="183.999" r="56"/>
                    <path fill="#1D71B8" d="M255.999,8.001c136.966,0,248,111.033,248,248s-111.034,248-248,248
                        C255.999,504,435.668,195.435,255.999,8.001"/>
                </g>
            </svg>
        `;
        
        toggleButton.innerHTML = sunSVG + moonSVG;

        // Find the navigation content container and add the button
        const navContent = document.querySelector('.nav-content');
        if (navContent) {
            navContent.appendChild(toggleButton);
        } else {
            // Fallback: try to find nav-container
            const navContainer = document.querySelector('.nav-container');
            if (navContainer) {
                navContainer.appendChild(toggleButton);
            } else {
                // Last fallback: add to body
                document.body.appendChild(toggleButton);
                toggleButton.style.position = 'fixed';
                toggleButton.style.top = '0.3rem';
                toggleButton.style.right = '3rem';
                toggleButton.style.zIndex = '9999';
            }
        }
    }

    bindEvents() {
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', () => this.toggleTheme());
        }

        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            if (!this.hasUserPreference()) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    toggleTheme() {
        const currentTheme = this.getCurrentTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
        this.saveTheme(newTheme);
    }

    setTheme(theme) {
        const html = document.documentElement;
        const toggleButton = document.getElementById('theme-toggle');

        if (theme === 'dark') {
            html.classList.add(this.darkModeClass);
            if (toggleButton) {
                toggleButton.setAttribute('data-theme', 'dark');
                toggleButton.setAttribute('aria-label', 'Switch to light mode');
                // In dark mode, show sun icon (to switch to light)
                toggleButton.querySelector('.sun-icon').style.display = 'block';
                toggleButton.querySelector('.moon-icon').style.display = 'none';
            }
        } else {
            html.classList.remove(this.darkModeClass);
            if (toggleButton) {
                toggleButton.setAttribute('data-theme', 'light');
                toggleButton.setAttribute('aria-label', 'Switch to dark mode');
                // In light mode, show moon icon (to switch to dark)
                toggleButton.querySelector('.sun-icon').style.display = 'none';
                toggleButton.querySelector('.moon-icon').style.display = 'block';
            }
        }

        // Dispatch custom event for other components to listen
        window.dispatchEvent(new CustomEvent('themechange', {
            detail: { theme }
        }));
    }

    getCurrentTheme() {
        return document.documentElement.classList.contains(this.darkModeClass) ? 'dark' : 'light';
    }

    getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    saveTheme(theme) {
        try {
            localStorage.setItem(this.storageKey, theme);
        } catch (e) {
            console.warn('Failed to save theme preference:', e);
        }
    }

    loadSavedTheme() {
        try {
            const savedTheme = localStorage.getItem(this.storageKey);
            if (savedTheme) {
                this.setTheme(savedTheme);
            } else {
                // Use system preference if no saved theme
                this.setTheme(this.getSystemTheme());
            }
        } catch (e) {
            console.warn('Failed to load theme preference:', e);
            // Fallback to system theme
            this.setTheme(this.getSystemTheme());
        }
    }

    hasUserPreference() {
        try {
            return localStorage.getItem(this.storageKey) !== null;
        } catch (e) {
            return false;
        }
    }
}

// Initialize dark mode toggle when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new DarkModeToggle();
    });
} else {
    new DarkModeToggle();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DarkModeToggle;
}