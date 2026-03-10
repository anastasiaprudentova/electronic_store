export const cartButton = document.getElementById('cart-button');
export const cartMenu = document.getElementById('cart-menu');
export const cartContainer = document.getElementById('cart-dropdown-container');

export const userButton = document.getElementById('user-button');
export const userMenu = document.getElementById('user-menu');
export const userContainer = document.getElementById('user-dropdown-container');

export const catalogButton = document.getElementById('catalog-button');
export const catalogMenu = document.getElementById('catalog-menu');
export const catalogContainer = document.getElementById('catalog-dropdown');

export const geoStatus = document.getElementById('geo-status');

export function getProductCards() {
    return document.querySelectorAll('.products-grid .product-card');
}

export function getAddToCartButtons() {
    return document.querySelectorAll('.add-to-cart');
}

export function getAddToFavoriteButtons() {
    return document.querySelectorAll('.add-to-favorite');
}