import { ref } from 'vue';

export const cart = ref([]);

export function findCartItem(productId) {
    return cart.value.find(item => item.id === productId);
}

export function addToCart(product) {
    const existing = findCartItem(product.id);
    if (existing) {
        existing.quantity++;
    } else {
        cart.value.push({ ...product, quantity: 1 });
    }
}

export function removeFromCart(productId) {
    const index = cart.value.findIndex(item => item.id === productId);
    if (index !== -1) {
        cart.value.splice(index, 1);
    }
}