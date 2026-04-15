import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from apps.orders.models import Order


@pytest.mark.django_db
class TestOrderManagerCombinations:
    """Тесты комбинирования методов OrderManager"""

    def test_chain_filter_methods(self, user, address):
        """
        Комбинирование фильтров по статусу и дате
        Ожидаемый результат: методы можно вызывать последовательно
        """
        paid_today = Order.objects.create(user=user, address=address, order_number="ORD-001", status='paid',
                                          total_amount=1000)
        paid_yesterday = Order.objects.create(user=user, address=address, order_number="ORD-002", status='paid',
                                              total_amount=2000)
        paid_yesterday.created_at = timezone.now() - timedelta(days=1)
        paid_yesterday.save()
        new_today = Order.objects.create(user=user, address=address, order_number="ORD-003", status='new',
                                         total_amount=3000)

        result = Order.objects.paid().created_today()
        assert paid_today in result and paid_yesterday not in result and new_today not in result
        assert result.count() == 1

    def test_chain_multiple_filters(self, user, address):
        """
        Комбинирование нескольких фильтров
        Ожидаемый результат: можно комбинировать фильтры по статусу, дате и пользователю
        """
        user_paid_today = Order.objects.create(user=user, address=address, order_number="ORD-001", status='paid',
                                               total_amount=1000)
        user_paid_yesterday = Order.objects.create(user=user, address=address, order_number="ORD-002", status='paid',
                                                   total_amount=2000)
        user_paid_yesterday.created_at = timezone.now() - timedelta(days=1)
        user_paid_yesterday.save()

        other_user = User.objects.create_user(username="other", password="123")
        other_paid_today = Order.objects.create(user=other_user, address=address, order_number="ORD-003", status='paid',
                                                total_amount=3000)

        result = Order.objects.by_user(user).paid().created_today()
        assert user_paid_today in result and user_paid_yesterday not in result and other_paid_today not in result
        assert result.count() == 1

    def test_chain_filter_with_aggregation(self, user, address):
        """
        Комбинирование фильтров с агрегацией
        Ожидаемый результат: агрегация применяется к отфильтрованным данным
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='paid', total_amount=1000)
        Order.objects.create(user=user, address=address, order_number="ORD-002", status='paid', total_amount=2000)
        yesterday = Order.objects.create(user=user, address=address, order_number="ORD-003", status='paid',
                                         total_amount=3000)
        yesterday.created_at = timezone.now() - timedelta(days=1)
        yesterday.save()
        Order.objects.create(user=user, address=address, order_number="ORD-004", status='new', total_amount=4000)

        assert Order.objects.paid().created_today().average_paid_order_value() == 1500
        assert Order.objects.created_today().total_revenue() == 3000

    def test_chain_filters_with_empty_result(self, user, address):
        """
        Комбинирование фильтров с пустым результатом
        Ожидаемый результат: возвращается пустой QuerySet
        """
        Order.objects.create(user=user, address=address, order_number="ORD-001", status='new', total_amount=1000)
        assert Order.objects.by_user(user).paid().count() == 0