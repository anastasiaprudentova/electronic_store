import pytest
from django.db import IntegrityError
from datetime import timedelta
from django.utils import timezone
from apps.delivery.models import Delivery

@pytest.mark.django_db
class TestDeliveryDates:
    """Тесты работы с датами в доставке"""

    def test_delivery_date_valid_sequence(self, order, address):
        """
        Корректная последовательность дат
        Ожидаемый результат: дата доставки может быть позже даты отправки
        """
        now = timezone.now()
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address,
            shipped_at=now,
            delivered_at=now + timedelta(days=2)
        )
        assert delivery.delivered_at > delivery.shipped_at

    def test_delivery_date_invalid_sequence(self, order, address):
        """
        Некорректная последовательность дат
        Ожидаемый результат: дата доставки не может быть раньше даты отправки
        """
        now = timezone.now()
        with pytest.raises(IntegrityError):
            Delivery.objects.create(
                order=order,
                delivery_type='courier',
                address=address,
                shipped_at=now,
                delivered_at=now - timedelta(days=2)
            )

    def test_delivery_date_delivered_without_shipped(self, order, address):
        """
        Дата доставки без даты отправки
        Ожидаемый результат: нельзя указать дату доставки без даты отправки
        """
        now = timezone.now()
        with pytest.raises(IntegrityError):
            Delivery.objects.create(
                order=order,
                delivery_type='courier',
                address=address,
                shipped_at=None,
                delivered_at=now
            )

    def test_delivery_date_partial_dates(self, order, address):
        """
        Частичное заполнение дат
        Ожидаемый результат: можно указать только shipped_at
        """
        now = timezone.now()
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address,
            shipped_at=now,
            delivered_at=None
        )
        assert delivery.shipped_at == now
        assert delivery.delivered_at is None