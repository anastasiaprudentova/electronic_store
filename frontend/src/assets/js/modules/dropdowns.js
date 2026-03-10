export function initDropdowns() {
    const cartContainer = document.getElementById('cart-dropdown-container');
    const userContainer = document.getElementById('user-dropdown-container');
    const catalogContainer = document.getElementById('catalog-dropdown');

    const cartButton = document.getElementById('cart-button');
    const userButton = document.getElementById('user-button');
    const catalogButton = document.getElementById('catalog-button');

    const cartMenu = document.getElementById('cart-menu');
    const userMenu = document.getElementById('user-menu');
    const catalogMenu = document.getElementById('catalog-menu');

    if (!cartButton || !userButton || !catalogButton || !cartMenu || !userMenu || !catalogMenu) {
        console.warn('Dropdown elements not found');
        return;
    }

    function closeAllDropdowns() {
        cartMenu.classList.remove('show');
        userMenu.classList.remove('show');
        catalogMenu.classList.remove('show');
        if (catalogContainer) catalogContainer.classList.remove('show');
    }

    function toggleDropdown(menu, container) {
        const isOpen = menu.classList.contains('show');
        closeAllDropdowns();
        if (!isOpen) {
        menu.classList.add('show');
        if (container) container.classList.add('show');
        }
    }

    cartButton.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleDropdown(cartMenu, cartContainer);
    });

    userButton.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleDropdown(userMenu, userContainer);
    });

    catalogButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleDropdown(catalogMenu, catalogContainer);
    });

    document.addEventListener('click', (e) => {
        if (!cartContainer?.contains(e.target) && !userContainer?.contains(e.target) && !catalogContainer?.contains(e.target)) {
        closeAllDropdowns();
        }
    });

    [cartMenu, userMenu, catalogMenu].forEach(menu => {
        menu.addEventListener('click', (e) => e.stopPropagation());
    });
}