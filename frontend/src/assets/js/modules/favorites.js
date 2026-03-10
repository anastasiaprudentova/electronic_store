import { showToast } from '../utils/toast.js';

export function initFavorites() {
    const addToFavoriteButtons = document.querySelectorAll('.add-to-favorite');
    addToFavoriteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const productCard = btn.closest('.product-card');
        const productName = productCard.querySelector('h3').innerText;
        showToast(`Товар «${productName}» добавлен в избранное`, 'fa-solid fa-heart');
        });
    });
}