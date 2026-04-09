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
                        Каталог <font-awesome-icon :icon="['fa', 'chevron-down']"/>
                    </a>
                    <div class="dropdown-menu" :class="{ show: showCatalog }">
                        <div class="dropdown-header">Категории</div>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'mobile-screen-button']"/> Смартфоны</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'laptop']"/> Ноутбуки</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'tablet-screen-button']"/> Планшеты</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'clock']"/> Часы</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'headphones']"/> Аксессуары</a>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'tag']"/> Все товары</a>
                    </div>
                </div>
                <a href="#">Поддержка</a>
            </nav>

            <div class="user-actions">
                <div class="header-search">
                    <input type="text" placeholder="Поиск товаров...">
                    <button><font-awesome-icon :icon="['fa', 'magnifying-glass']"/></button>
                </div>

                <button class="icon-btn" @click="toggleTheme" :title="isDark ? 'Светлая тема' : 'Темная тема'">
                    <font-awesome-icon :icon="isDark ? ['fas', 'sun'] : ['fas', 'moon']" />
                </button>

                <div class="dropdown-container">
                    <button class="icon-btn" @click.prevent="toggleCart" title="Корзина">
                        <font-awesome-icon :icon="['fa', 'cart-shopping']"/>
                        <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
                    </button>
                    <div class="dropdown-menu" :class="{ show: showCart }">
                        <div class="dropdown-header">
                            <font-awesome-icon :icon="['fa', 'cart-shopping']" style="margin-right: 8px;"/> Корзина
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
                                        <font-awesome-icon :icon="['fa', 'trash']"/>
                                    </button>
                                </div>
                            </div>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item">
                            <font-awesome-icon :icon="['fa', 'arrow-right']"/><span>Перейти в корзину</span>
                        </a>
                    </div>
                </div>

                <div class="dropdown-container">
                    <button class="icon-btn" @click.prevent="toggleUser" title="Профиль">
                        <font-awesome-icon :icon="['fa', 'user']"/>
                    </button>
                    <div class="dropdown-menu" :class="{ show: showUser }">
                        <div class="dropdown-header">
                            <font-awesome-icon :icon="['fa', 'user']" style="margin-right: 8px;"/> Аккаунт
                        </div>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'id-card']"/> Профиль</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'box']"/> Заказы</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'heart']"/> Избранное</a>
                        <a href="#" class="dropdown-item"><font-awesome-icon :icon="['fa', 'gear']"/> Настройки</a>
                        <div class="dropdown-divider"></div>
                        <div class="geo-info">
                            <font-awesome-icon :icon="['fa', 'location-dot']"/>
                            <span>{{ geoStatus }}</span>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item">
                            <font-awesome-icon :icon="['fa', 'sign-out-alt']"/>  Выйти</a>
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