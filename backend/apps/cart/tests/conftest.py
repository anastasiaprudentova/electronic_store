import pytest
from django.contrib.auth.models import User
from apps.catalog.models import Brand, Category, Product, Variation
from apps.cart.models import Cart

@pytest.fixture
def user():
    """Фикстура: создает тестового пользователя"""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def brand():
    """Фикстура: создает тестовый бренд"""
    return Brand.objects.create(name="Samsung")


@pytest.fixture
def category():
    """Фикстура: создает тестовую категорию"""
    return Category.objects.create(name="Смартфоны")


@pytest.fixture
def product(brand, category):
    """Фикстура: создает тестовый товар"""
    return Product.objects.create(
        name="Galaxy S24",
        brand=brand,
        category=category,
        description="Флагманский смартфон"
    )


@pytest.fixture
def variation(product):
    """Фикстура: создает тестовую вариацию товара"""
    return Variation.objects.create(
        product=product,
        sku="S24-BLK-256",
        price=80000,
        is_active=True
    )


@pytest.fixture
def cart_item(user, variation):
    """Фикстура: создает тестовый элемент корзины"""
    return Cart.objects.create(
        user=user,
        variation=variation,
        quantity=2
    )