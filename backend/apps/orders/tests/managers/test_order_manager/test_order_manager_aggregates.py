import pytest
from apps.orders.models import Order

@pytest.mark.django_db
class TestOrderManagerAggregates:
    """Тесты агрегатных методов OrderManager"""

    def test_average_paid_order_value(self, user, address):
        """
        Средняя сумма оплаченных заказов
        Ожидаемый результат: возвращает среднее арифметическое сумм оплаченных заказов
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='paid', total_amount=1000)
        Order.objects.create(user=user, address=address, order_number="ORD-002", status='paid', total_amount=2000)
        Order.objects.create(user=user, address=address, order_number="ORD-003", status='new', total_amount=3000)
        assert Order.objects.average_paid_order_value() == 1500

    def test_average_paid_order_value_with_no_paid_orders(self, user, address):
        """
        Средняя сумма при отсутствии оплаченных заказов
        Ожидаемый результат: возвращает 0
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='new', total_amount=1000)
        assert Order.objects.average_paid_order_value() == 0

    def test_total_revenue(self, user, address):
        """
        Общая выручка по оплаченным заказам
        Ожидаемый результат: возвращает сумму всех оплаченных заказов
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='paid', total_amount=1000)
        Order.objects.create(user=user, address=address, order_number="ORD-002", status='paid', total_amount=2000)
        Order.objects.create(user=user, address=address, order_number="ORD-003", status='new', total_amount=3000)
        assert Order.objects.total_revenue() == 3000

    def test_total_revenue_with_no_paid_orders(self, user, address):
        """
        Выручка при отсутствии оплаченных заказов
        Ожидаемый результат: возвращает 0
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='new', total_amount=1000)
        assert Order.objects.total_revenue() == 0