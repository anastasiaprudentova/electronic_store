import pytest
from django.contrib.auth.models import User
from apps.users.models import Address

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
        recipient_name="Иван Петров",
        phone="+7-999-123-45-67",
        city="Москва",
        street="Ленина",
        house="10",
        apartment="5",
        postal_code="123456",
        is_default=True
    )


@pytest.fixture
def second_address(user):
    """Фикстура: создает второй тестовый адрес"""
    return Address.objects.create(
        user=user,
        recipient_name="Петр Иванов",
        city="Санкт-Петербург",
        street="Невский",
        house="20",
        apartment="15",
        is_default=False
    )