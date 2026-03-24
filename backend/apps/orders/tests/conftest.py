import pytest
from django.contrib.auth.models import User
from apps.users.models import Address
from apps.catalog.models import Product, Brand, Category, Variation
from apps.orders.models import PickupPoint, Order, OrderItem

@pytest.fixture
def user():
    """Фикстура: создает тестового пользователя"""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def address(user):
    """Фикстура: создает тестовый адрес"""
    return Address.objects.create(
        user=user,
        recipient_name="Тест Тестов",
        city="Москва",
        street="Ленина",
        house="10",
        apartment="5",
        is_default=True
    )


@pytest.fixture
def pickup_point():
    """Фикстура: создает тестовый пункт выдачи"""
    return PickupPoint.objects.create(
        name="ПВЗ на Ленина",
        carrier="СДЭК",
        city="Москва",
        address="ул. Ленина, д. 15",
        working_hours="пн-пт 10-20",
        is_active=True
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
    """Фикстура: создает тестовую вариацию"""
    return Variation.objects.create(
        product=product,
        sku="S24-BLK-256",
        price=80000,
        is_active=True
    )


@pytest.fixture
def order(user, address):
    """Фикстура: создает тестовый заказ"""
    return Order.objects.create(
        user=user,
        address=address,
        order_number="ORD-001",
        status="new",
        total_amount=5000,
        comment="Тестовый заказ"
    )


@pytest.fixture
def order_item(order, variation):
    """Фикстура: создает тестовую позицию заказа"""
    return OrderItem.objects.create(
        order=order,
        variation=variation,
        quantity=2,
        price_per_unit=80000,
        total_price=160000
    )


@pytest.fixture
def paid_order(user, address):
    """Фикстура: создает оплаченный заказ"""
    return Order.objects.create(
        user=user,
        address=address,
        order_number="ORD-002",
        status="paid",
        total_amount=15000
    )


@pytest.fixture
def processing_order(user, address):
    """Фикстура: создает заказ в обработке"""
    return Order.objects.create(
        user=user,
        address=address,
        order_number="ORD-003",
        status="processing",
        total_amount=25000
    )