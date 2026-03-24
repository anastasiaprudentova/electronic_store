import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.orders.models import Order
from datetime import timedelta
from django.utils import timezone

@pytest.mark.django_db
class TestOrderModel:
    """Тестирование модели Order (заказы)"""

    def test_create_order_with_valid_data(self, user, address):
        """
        Создание заказа с валидными данными
        Ожидаемый результат: заказ создается со всеми полями
        """
        order = Order.objects.create(
            user=user,
            address=address,
            order_number="ORD-123456",
            total_amount=10000,
            comment="Тестовый заказ"
        )
        assert order.order_number == "ORD-123456"
        assert order.total_amount == 10000
        assert order.created_at is not None

    def test_order_unique_order_number(self, user, address):
        """
        Уникальность номера заказа
        Ожидаемый результат: нельзя создать два заказа с одинаковым номером
        """
        Order.objects.create(user=user, address=address, order_number="ORD-123456", total_amount=10000)
        with pytest.raises(IntegrityError):
            Order.objects.create(user=user, address=address, order_number="ORD-123456", total_amount=20000)

    def test_order_validators_order_number_format(self, user, address):
        """
        Валидация формата номера заказа
        Ожидаемый результат: номер должен содержать только заглавные буквы, цифры и дефис
        """
        for number in ["ORD-123", "TEST-001", "ABC123"]:
            order = Order.objects.create(user=user, address=address, order_number=number, total_amount=10000)
            assert order.order_number == number

    def test_order_status_choices(self, user, address):
        """
        Проверка допустимых статусов заказа
        Ожидаемый результат: можно установить любой из допустимых статусов
        """
        for status in ['new', 'processing', 'paid', 'shipped', 'delivered', 'cancelled']:
            order = Order.objects.create(
                user=user, address=address, order_number=f"ORD-{status}",
                status=status, total_amount=10000
            )
            assert order.status == status

    def test_order_total_amount_validation(self, user, address):
        """
        Валидация суммы заказа
        Ожидаемый результат: сумма не может быть отрицательной
        """
        with pytest.raises(ValidationError):
            order = Order(user=user, address=address, order_number="ORD-001", total_amount=-1000)
            order.full_clean()

    def test_order_str_method(self, order):
        """
        Строковое представление заказа
        Ожидаемый результат: __str__ возвращает "Заказ №{order_number}"
        """
        assert str(order) == f"Заказ №{order.order_number}"

    def test_order_ordering(self, user, address):
        """
        Сортировка заказов по умолчанию (новые сверху)
        Ожидаемый результат: заказы сортируются по убыванию даты создания
        """
        old = Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=1000)
        old.created_at = timezone.now() - timedelta(days=5)
        old.save()

        new = Order.objects.create(user=user, address=address, order_number="ORD-002", total_amount=2000)

        orders = Order.objects.all()
        assert orders[0] == new
        assert orders[1] == old

    def test_order_comment_optional(self, user, address):
        """
        Комментарий к заказу необязателен
        Ожидаемый результат: можно создать заказ без комментария
        """
        order = Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=10000)
        assert order.comment == ""

    def test_order_on_delete_protect_user(self, user, address):
        """
        Защита от удаления пользователя с заказами
        Ожидаемый результат: нельзя удалить пользователя, у которого есть заказы
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=10000)
        with pytest.raises(IntegrityError):
            user.delete()