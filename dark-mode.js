/**
 * Dark Mode Toggle — light ↔ dark, persisted in localStorage.
 */
(function() {
    'use strict';

    const STORAGE_KEY = 'theme-preference';
    const root = document.documentElement;
    const toggle = document.getElementById('theme-toggle');

    function systemPrefersDark() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    function readInitialTheme() {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored === 'light' || stored === 'dark') return stored;
        return systemPrefersDark() ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        if (theme === 'dark') root.classList.add('dark-mode');
        else root.classList.remove('dark-mode');
        if (toggle) toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    }

    let currentTheme = readInitialTheme();
    applyTheme(currentTheme);

    function toggleTheme() {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, currentTheme);
        applyTheme(currentTheme);
    }

    if (toggle) {
        toggle.addEventListener('click', toggleTheme);
        toggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }

    window.addEventListener('storage', (e) => {
        if (e.key === STORAGE_KEY && (e.newValue === 'light' || e.newValue === 'dark')) {
            currentTheme = e.newValue;
            applyTheme(currentTheme);
        }
    });
})();
