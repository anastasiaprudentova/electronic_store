import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from apps.orders.models import Order

@pytest.mark.django_db
class TestOrderManagerFilters:
    """Тесты методов фильтрации OrderManager"""

    def test_created_today_returns_today_orders(self, user, address):
        """
        Фильтр заказов за сегодня
        Ожидаемый результат: возвращает только заказы, созданные сегодня
        """
        today = Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=1000)
        yesterday = Order.objects.create(user=user, address=address, order_number="ORD-002", total_amount=2000)
        yesterday.created_at = timezone.now() - timedelta(days=1)
        yesterday.save()
        result = Order.objects.created_today()
        assert today in result and yesterday not in result

    def test_last_days_returns_orders_from_last_n_days(self, user, address):
        """
        Фильтр заказов за последние N дней
        Ожидаемый результат: возвращает заказы, созданные за указанный период
        """
        old = Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=1000)
        old.created_at = timezone.now() - timedelta(days=5)
        old.save()
        recent = Order.objects.create(user=user, address=address, order_number="ORD-002", total_amount=2000)
        recent.created_at = timezone.now() - timedelta(days=2)
        recent.save()
        result = Order.objects.last_days(days=3)
        assert recent in result and old not in result

    def test_by_user_returns_user_orders(self, user, address):
        """
        Фильтр заказов по пользователю
        Ожидаемый результат: возвращает только заказы указанного пользователя
        """
        order = Order.objects.create(user=user, address=address, order_number="ORD-001", total_amount=1000)
        other = User.objects.create_user(username="other", password="123")
        other_order = Order.objects.create(user=other, address=address, order_number="ORD-002", total_amount=2000)
        result = Order.objects.by_user(user)
        assert order in result and other_order not in result

    def test_new_paid_processing_filters(self, order, paid_order, processing_order):
        """
        Фильтры по статусам заказов
        Ожидаемый результат: new() возвращает новые, paid() возвращает оплаченные,
        processing() возвращает заказы в обработке
        """
        assert order in Order.objects.new()
        assert paid_order in Order.objects.paid()
        assert processing_order in Order.objects.processing()

    def test_by_status_returns_orders_with_given_status(self, order, paid_order):
        """
        Фильтр по произвольному статусу
        Ожидаемый результат: возвращает заказы с указанным статусом
        """
        assert order in Order.objects.by_status('new')
        assert paid_order in Order.objects.by_status('paid')