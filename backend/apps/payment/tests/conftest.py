import pytest
from django.contrib.auth.models import User
from apps.users.models import Address
from apps.orders.models import Order

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
        apartment="5"
    )


@pytest.fixture
def order(user, address):
    """Фикстура: создает тестовый заказ"""
    return Order.objects.create(
        user=user,
        address=address,
        order_number="ORD-001",
        status='new',
        total_amount=5000
    )