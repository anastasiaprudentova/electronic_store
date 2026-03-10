<template>
    <header>
        <div class="container header-inner">
            <div class="logo-area">
                    <router-link to="/">
                    <img src="@/assets/image/icons/logo.svg" alt="logo">
                    </router-link>
            </div>

            <nav class="main-nav">
                <div class="dropdown-container">
                    <a href="#" class="catalog-link" @click.prevent="toggleCatalog">
                        Каталог <i class="fa-solid fa-chevron-down"></i>
                    </a>
                    <div class="dropdown-menu" :class="{ show: showCatalog }">
                        <div class="dropdown-header">Категории</div>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-mobile-screen-button"></i> Смартфоны</a>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-laptop"></i> Ноутбуки</a>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-tablet-screen-button"></i> Планшеты</a>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-clock"></i> Часы</a>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-headphones"></i> Аксессуары</a>
                        <div class="dropdown-divider"></div>
                        <router-link to="#" class="dropdown-item"><i class="fa-solid fa-tag"></i> Все товары</router-link>
                    </div>
                </div>
                <a href="#">Поддержка</a>
            </nav>

            <div class="user-actions">
                <div class="header-search">
                    <input type="text" placeholder="Поиск товаров...">
                    <button><i class="fa-solid fa-magnifying-glass"></i></button>
                </div>

                <button class="icon-btn" @click="toggleTheme" :title="isDark ? 'Светлая тема' : 'Темная тема'">
                    <i :class="isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
                </button>

                <div class="dropdown-container">
                    <button class="icon-btn" @click.prevent="toggleCart" title="Корзина">
                        <i class="fa-solid fa-cart-shopping"></i>
                        <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
                    </button>
                    <div class="dropdown-menu" :class="{ show: showCart }">
                        <div class="dropdown-header">
                            <i class="fa-solid fa-cart-shopping" style="margin-right: 8px;"></i> Корзина
                        </div>
                        <div class="cart-preview">
                            <div v-if="cart.length === 0" class="cart-preview-empty">Корзина пуста</div>
                                <div v-else v-for="item in cart" :key="item.id" class="cart-preview-item">
                                    <div class="cart-preview-image" :style="{ backgroundImage: `url('${item.image}')` }"></div>
                                    <div class="cart-preview-info">
                                        <div class="cart-preview-title">{{ item.name }}</div>
                                        <div class="cart-preview-price">{{ (item.price * item.quantity).toLocaleString() }} ₽</div>
                                        <div class="cart-preview-quantity">Количество: {{ item.quantity }}</div>
                                    </div>
                                    <button class="cart-preview-remove" @click="removeFromCart(item.id)" title="Удалить">
                                        <i class="fa-solid fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        <div class="dropdown-divider"></div>
                        <router-link to="#" class="dropdown-item">
                            <i class="fa-solid fa-arrow-right"></i> <span>Перейти в корзину</span>
                        </router-link>
                    </div>
                </div>

                <div class="dropdown-container">
                    <button class="icon-btn" @click.prevent="toggleUser" title="Профиль">
                        <i class="fa-solid fa-user"></i>
                    </button>
                    <div class="dropdown-menu" :class="{ show: showUser }">
                        <div class="dropdown-header">
                            <i class="fa-solid fa-user" style="margin-right: 8px;"></i> Аккаунт
                        </div>
                        <router-link to="#" class="dropdown-item"><i class="fa-solid fa-id-card"></i> Профиль</router-link>
                        <router-link to="#" class="dropdown-item"><i class="fa-solid fa-box"></i> Заказы</router-link>
                        <router-link to="#" class="dropdown-item"><i class="fa-solid fa-heart"></i> Избранное</router-link>
                        <router-link to="#" class="dropdown-item"><i class="fa-solid fa-gear"></i> Настройки</router-link>
                        <div class="dropdown-divider"></div>
                        <div class="geo-info">
                            <i class="fa-solid fa-location-dot"></i>
                            <span>{{ geoStatus }}</span>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item"><i class="fa-solid fa-sign-out-alt"></i> Выйти</a>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { cart, removeFromCart } from '@/assets/js/modules/cart.js';
import { setTheme } from '@/assets/js/modules/theme.js';
import { requestGeolocation } from '@/assets/js/modules/geolocation.js';

const showCatalog = ref(false);
const showCart = ref(false);
const showUser = ref(false);
const isDark = ref(false);
const geoStatus = ref('Определение местоположения...');
const geoRequested = ref(false);

const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0));

function toggleTheme() {
    isDark.value = !isDark.value;
    setTheme(isDark.value);
}

function closeAllDropdowns() {
    showCatalog.value = false;
    showCart.value = false;
    showUser.value = false;
}

function toggleCatalog() {
    if (showCatalog.value) {
        showCatalog.value = false;
    } else {
        closeAllDropdowns();
        showCatalog.value = true;
    }
}

function toggleCart() {
    if (showCart.value) {
        showCart.value = false;
    } else {
        closeAllDropdowns();
        showCart.value = true;
    }
}

function toggleUser() {
    if (showUser.value) {
        showUser.value = false;
    } else {
        closeAllDropdowns();
        showUser.value = true;
        if (!geoRequested.value) {
            requestGeolocation()
                .then(city => {
                    geoStatus.value = city;
                    geoRequested.value = true;
                })
                .catch(() => {
                    geoStatus.value = 'Город не определён';
                });
            }
    }
}

function handleClickOutside(e) {
    if (!e.target.closest('header')) {
        closeAllDropdowns();
    }
}

onMounted(() => {
    const saved = localStorage.getItem('theme');
    isDark.value = saved === 'dark' || (saved === null && window.matchMedia('(prefers-color-scheme: dark)').matches);
    setTheme(isDark.value);

    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});
</script>