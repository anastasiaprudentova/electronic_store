<template>
    <main>
        <section class="container hero fade-in">
            <div class="hero-grid">
                <div class="hero-content">
                    <h2>Новые телефоны уже здесь.</h2>
                    <p>Флагманские модели с мощными процессорами, улучшенными камерами и стильным дизайном. Успейте оценить инновации первыми!</p>
                    <a href="#" class="btn">ПЕРЕЙТИ</a>
                </div>
                <div class="hero-images">
                    <img src="@/assets/image/phone-hero.webp" alt="Hero image">
                </div>
            </div>
        </section>

        <section class="container">
            <h2 class="section-title">Популярные категории</h2>
            <div class="parent">
                <div class="div1 fade-in">
                    <img class="img-laptop" src="@/assets/image/laptop-catalog.webp" alt="laptop">
                    <div class="category-text"><p>Ноутбуки</p><h3>Для продуктивной работы</h3></div>
                </div>
                <div class="div2 fade-in">
                    <img class="img-watch" src="@/assets/image/watch-catalog.webp" alt="watch">
                    <div class="category-text"><p>Часы</p><h3>Стиль и качество</h3></div>
                </div>
                <div class="div3 fade-in">
                    <img class="img-tablet" src="@/assets/image/tablet-catalog.webp" alt="tablet">
                    <div class="category-text"><p>Планшеты</p><h3>Мобильность для работы</h3></div>
                </div>
                <div class="div4 fade-in">
                    <img class="img-phone" src="@/assets/image/phone-catalog.webp" alt="phone">
                    <div class="category-text"><p>Смартфоны</p><h3>Для повседневной жизни</h3></div>
                </div>
            </div>
        </section>

        <section class="container">
            <h2 class="section-title">Новые поступления</h2>
            <div class="products-grid">
                <div v-for="product in products" :key="product.id" class="product-card fade-in">
                <div class="product-badge">Новинка</div>
                <div class="product-image" :style="{ backgroundImage: `url('${product.image}')` }"></div>
                <div class="product-info">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <div class="product-rating" v-html="renderRating(product.rating, product.reviews)"></div>
                    <div class="price-wrapper">
                        <span class="price">{{ product.price.toLocaleString() }} ₽</span>
                        <div class="product-actions">
                            <button class="action-btn add-to-cart" @click="addToCartHandler(product)" title="Добавить в корзину">
                                <font-awesome-icon :icon="['fa', 'cart-shopping']"/>
                            </button>
                            <button class="action-btn add-to-favorite" @click="addToFavoriteHandler(product.name)" title="В избранное">
                                <font-awesome-icon :icon="['fa', 'heart']"/>
                            </button>
                        </div>
                    </div>
                </div>
                </div>
            </div>
        </section>

        <section class="container search-block fade-in">
            <h3 class="search-title">Не нашли нужный товар?</h3>
            <div class="search-field">
                <input type="text" placeholder="Введите название...">
                <button type="button">
                    <font-awesome-icon :icon="['fa', 'magnifying-glass']"/>
                </button>
            </div>
            <div class="brand-tags">
                <span class="tag" v-for="tag in tags" :key="tag">
                    {{ tag }}
                </span>
            </div>
        </section>

        <section class="container special-order fade-in">
            <div class="order-info">
                <h3>Закажем нужный товар специально для вас</h3>
                <p>Оставьте свой email, и мы подберём идеальный гаджет</p>
                <form class="order-form" @submit.prevent="submitOrder">
                    <input type="email" placeholder="example@yandex.ru" v-model="orderEmail">
                    <textarea placeholder="Введите название модели..." v-model="orderModel"></textarea>
                    <button type="submit" class="btn">ОТПРАВИТЬ</button>
                </form>
            </div>
            <div class="order-images">
                <img src="@/assets/image/phone-form.webp" alt="Смартфон" class="phone">
            </div>
        </section>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { addToCart } from '@/assets/js/modules/cart.js';
import { showToast } from '@/assets/js/utils/toast.js';
import { renderRating } from '@/assets/js/modules/rating.js';

import laptopCard from '@/assets/image/laptop-orders.webp';
import watchCard from '@/assets/image/watch-orders.webp';
import tabletCard from '@/assets/image/tablet-orders.webp';

defineOptions({ name: 'MainPage' });

const products = ref([
    {
        id: 1,
        name: 'MateBook X Pro',
        description: 'Молниеносная скорость работы, вдохновляющий дизайн',
        price: 180000,
        image: laptopCard,
        rating: 0,
        reviews: 0
    },
    {
        id: 2,
        name: 'Watch GT 6 Pro',
        description: 'Продвинутые режимы для занятия спортом на открытом воздухе',
        price: 20000,
        image: watchCard,
        rating: 0,
        reviews: 0
    },
    {
        id: 3,
        name: 'MatePad 11,5 S',
        description: 'Элегантный дизайн планшета позволяет сохранить производительность',
        price: 32000,
        image: tabletCard,
        rating: 0,
        reviews: 0
    }
]);

const tags = ref([
    'Huawei', 'Xiaomi', 'Часы', 'Google Pixel 9', 'Клавиатура',
    'OPPO Find', 'iPhone 16', 'Ноутбук', 'Смартфон'
]);

const orderEmail = ref('');
const orderModel = ref('');

function addToCartHandler(product) {
    addToCart(product);
    showToast(`Товар «${product.name}» добавлен в корзину`, 'fa-solid fa-cart-shopping');
}

function addToFavoriteHandler(productName) {
    showToast(`Товар «${productName}» добавлен в избранное`, 'fa-solid fa-heart');
}

function submitOrder() {
    showToast('Заявка отправлена', 'fa-solid fa-check');
    orderEmail.value = '';
    orderModel.value = '';
}

function initScrollAnimations() {
    const elements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
            entry.target.classList.add('visible');
            }, index * 70);
            observer.unobserve(entry.target);
        }
        });
    }, { threshold: 0.2, rootMargin: '0px 0px -80px 0px' });
    elements.forEach(el => observer.observe(el));
}

onMounted(() => {
    initScrollAnimations();
});
</script>