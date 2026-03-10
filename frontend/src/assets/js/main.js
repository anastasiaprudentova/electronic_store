import { initTheme } from './modules/theme.js';
import { initScrollAnimations } from './utils/ui.js';
import { initRatings } from './modules/rating.js';
import { initCart } from './modules/cart.js';
import { initDropdowns } from './modules/dropdowns.js';
import { initGeolocation } from './modules/geolocation.js';
import { initFavorites } from './modules/favorites.js';

document.addEventListener('DOMContentLoaded', () => {
    initCart();
    initDropdowns();
    initGeolocation();
    initFavorites();
    initTheme();
});

window.addEventListener('load', () => {
    initScrollAnimations();
    initRatings();
});