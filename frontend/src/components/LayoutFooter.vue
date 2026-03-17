<template>
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <div class="logo-area" style="margin-bottom: 15px;">
                        <div class="logo-placeholder" style="width: 40px; height: 40px;">
                            <img src="@/assets/image/icons/logo.svg" alt="logo" onerror="this.style.display='none'; this.parentElement.innerHTML='<i class=\'fa-solid fa-bolt\' style=\'font-size:24px;color:#2e5f6b\'></i>';">
                        </div>
                        <span style="font-weight: 600; font-size: 20px; color: var(--text);">Электрополис</span>
                    </div>
                    <p>Самый лучший магазин гаджетов в этой и далекой далекой галактиках. Более 10 000 товаров в наличии.</p>
                    <div class="contact-item">
                        <i class="fa-solid fa-phone"></i>
                        <span>8 (800) 123-45-67</span>
                    </div>
                    <div class="contact-item">
                        <i class="fa-solid fa-envelope"></i>
                        <span>info@electropolis.ru</span>
                    </div>
                    <div class="contact-item">
                        <i class="fa-solid fa-location-dot"></i>
                        <span>г. Владимир, ул. Сакко и Винцетти, д. 1</span>
                    </div>
                </div>

                <div class="footer-col">
                    <h4>Информация</h4>
                    <ul>
                        <li><a href="#">О нас</a></li>
                        <li><a href="#">Доставка и оплата</a></li>
                        <li><a href="#">Гарантия и возврат</a></li>
                        <li><a href="#">Политика конфиденциальности</a></li>
                        <li><a href="#">Публичная оферта</a></li>
                        <li><a href="#">Контакты</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h4>Будьте в курсе</h4>
                    <p>Подпишитесь на новости и получите скидку 10% на первый заказ!</p>
                    <form class="subscribe-form">
                        <input type="email" placeholder="Ваш email" required>
                        <button type="submit">Подписаться</button>
                    </form>
                    <div class="social-links">
                        <a href="#"><i class="fa-brands fa-vk"></i></a>
                        <a href="#"><i class="fa-brands fa-telegram"></i></a>
                        <a href="#"><i class="fa-brands fa-odnoklassniki"></i></a>
                        <a href="#"><i class="fa-brands fa-youtube"></i></a>
                    </div>
                </div>
            </div>

            <div class="payment-methods">
                <i class="fa-brands fa-cc-visa"></i>
                <i class="fa-brands fa-cc-mastercard"></i>
                <img src="@/assets/image/icons/mir-pay.svg" alt="mir-pay">
                <i class="fa-brands fa-cc-paypal"></i>
                <i class="fa-brands fa-cc-apple-pay"></i>
                <i class="fa-brands fa-cc-google-pay"></i>
            </div>

            <div class="copyright">
                © 2026 Электрополис. Все права защищены. Denizer1305 & Anastasia_Qe
            </div>
        </div>
    </footer>

    <div class="toast-container" id="toast-container"></div>
</template>

<script setup>
    defineOptions({ name: 'LayoutFooter' });
</script>