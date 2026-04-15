import pytest
from django.contrib.auth.models import User
from apps.catalog.models import Brand, Category, Product, Variation, Stock
from apps.reviews.models import Review

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
        name="Galaxy S20",
        brand=brand,
        category=category,
        description="Флагманский смартфон Samsung"
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
def stock(variation):
    """Фикстура: создает тестовый остаток на складе"""
    return Stock.objects.create(
        variation=variation,
        warehouse_id=1,
        quantity=10,
        reserved=2
    )

@pytest.fixture
def review(user, product):
    """Фикстура: создает тестовый отзыв"""
    return Review.objects.create(
        user=user,
        product=product,
        rating=5,
        comment="Отличный товар!",
        is_moderated=True
    )