/**
 * Theme Manager - Dark/Light Mode Toggle
 */

const THEME_KEY = 'infinexpense-theme';
const LIGHT_THEME = 'light';
const DARK_THEME = 'dark';

/**
 * Initialize theme on page load
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY) || DARK_THEME;
    applyTheme(savedTheme);
    
    // Wait a bit for template to be injected before setting up toggle
    setTimeout(() => {
        setupThemeToggle();
    }, 150);
}

/**
 * Apply theme to document
 */
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeToggleIcon(theme);
    localStorage.setItem(THEME_KEY, theme);
}

/**
 * Toggle between themes
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || DARK_THEME;
    const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    applyTheme(newTheme);
}

/**
 * Update theme toggle icon display
 */
function updateThemeToggleIcon(theme, retryCount = 0) {
    const darkIcon = document.querySelector('.theme-icon-dark');
    const lightIcon = document.querySelector('.theme-icon-light');
    
    console.log('Updating icons for theme:', theme, {darkIcon, lightIcon});
    
    if (darkIcon && lightIcon) {
        if (theme === LIGHT_THEME) {
            darkIcon.style.display = 'none';
            lightIcon.style.display = 'inline';
            console.log('Switched to light mode - showing sun icon');
        } else {
            darkIcon.style.display = 'inline';
            lightIcon.style.display = 'none';
            console.log('Switched to dark mode - showing moon icon');
        }
    } else if (retryCount < 3) {
        console.warn('Icons not found, retrying...', {darkIcon, lightIcon, retryCount});
        setTimeout(() => updateThemeToggleIcon(theme, retryCount + 1), 150);
    } else {
        console.warn('Icons not found after retries', {darkIcon, lightIcon});
    }
}

/**
 * Setup theme toggle button event listener
 */
function setupThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Remove any existing listeners to avoid duplicates
        themeToggle.removeEventListener('click', toggleTheme);
        themeToggle.addEventListener('click', toggleTheme);
        console.log('Theme toggle button initialized');
    } else {
        console.warn('Theme toggle button not found - retrying...');
        // Retry after a delay if button not found
        setTimeout(setupThemeToggle, 200);
    }
}

// Initialize theme when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeTheme);
} else {
    initializeTheme();
}
