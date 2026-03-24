import pytest
from django.contrib.auth.models import User
from apps.catalog.models import Brand, Category, Product
from apps.wishlist.models import Wishlist

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
def wishlist(user, product):
    """Фикстура: создает тестовую запись в избранном"""
    return Wishlist.objects.create(user=user, product=product)