export function setTheme(isDark) {
    if (isDark) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

export function loadTheme() {
    const saved = localStorage.getItem('theme');
    if (saved !== null) {
        setTheme(saved === 'dark');
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setTheme(true);
    }
}