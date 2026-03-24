import pytest
from django.contrib.auth.models import User
from apps.catalog.models import Brand, Category, Product
from apps.reviews.models import Review

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="test@example.com", password="123")


@pytest.fixture
def brand():
    return Brand.objects.create(name="Samsung")


@pytest.fixture
def category():
    return Category.objects.create(name="Смартфоны")


@pytest.fixture
def product(brand, category):
    return Product.objects.create(
        name="Galaxy S24",
        brand=brand,
        category=category,
        description="Флагманский смартфон"
    )


@pytest.fixture
def review(user, product):
    return Review.objects.create(
        user=user,
        product=product,
        rating=5,
        comment="Отличный товар!",
        is_moderated=True
    )


@pytest.fixture
def unmoderated_review(user, product):
    """Создаем непроверенный отзыв для другого товара, чтобы избежать конфликта"""
    other_product = Product.objects.create(
        name="Другой товар",
        brand=brand,
        category=category
    )
    return Review.objects.create(
        user=user,
        product=other_product,
        rating=4,
        comment="Хороший товар",
        is_moderated=False
    )