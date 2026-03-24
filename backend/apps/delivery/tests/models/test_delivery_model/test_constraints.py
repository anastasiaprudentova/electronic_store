import pytest
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from apps.delivery.models import Delivery

@pytest.mark.django_db
class TestDeliveryConstraints:
    """Тестирование constraints модели Delivery"""

    def test_courier_requires_address(self, order):
        """
        Курьерская доставка требует адрес
        Ожидаемый результат: ошибка при создании без address
        """
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='courier')

    def test_courier_cannot_have_pickup(self, order, address, pickup_point):
        """
        Курьерская доставка не может иметь пункт выдачи
        Ожидаемый результат: ошибка при наличии pickup_point
        """
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='courier',
                                    address=address, pickup_point=pickup_point)

    def test_pickup_requires_point(self, order):
        """
        Доставка в ПВЗ требует пункт выдачи
        Ожидаемый результат: ошибка при создании без pickup_point
        """
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='pickup')

    def test_pickup_cannot_have_address(self, order, address, pickup_point):
        """
        Доставка в ПВЗ не может иметь адрес
        Ожидаемый результат: ошибка при наличии address
        """
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='pickup',
                                    address=address, pickup_point=pickup_point)

    def test_valid_courier(self, order, address):
        """
        Валидная курьерская доставка
        Ожидаемый результат: создается без ошибок
        """
        delivery = Delivery.objects.create(order=order, delivery_type='courier', address=address)
        assert delivery.delivery_type == 'courier' and delivery.address == address

    def test_valid_pickup(self, order, pickup_point):
        """
        Валидная доставка в ПВЗ
        Ожидаемый результат: создается без ошибок
        """
        delivery = Delivery.objects.create(order=order, delivery_type='pickup', pickup_point=pickup_point)
        assert delivery.delivery_type == 'pickup' and delivery.pickup_point == pickup_point

    def test_date_valid(self, order, address):
        """
        Корректная последовательность дат
        Ожидаемый результат: delivered_at позже shipped_at
        """
        now = timezone.now()
        delivery = Delivery.objects.create(order=order, delivery_type='courier', address=address,
                                           shipped_at=now, delivered_at=now + timedelta(days=2))
        assert delivery.delivered_at > delivery.shipped_at

    def test_date_equal(self, order, address):
        """
        Равные даты отправки и доставки
        Ожидаемый результат: допускается
        """
        now = timezone.now()
        delivery = Delivery.objects.create(order=order, delivery_type='courier', address=address,
                                           shipped_at=now, delivered_at=now)
        assert delivery.delivered_at == delivery.shipped_at

    def test_date_invalid(self, order, address):
        """
        Некорректная последовательность дат
        Ожидаемый результат: ошибка при delivered_at раньше shipped_at
        """
        now = timezone.now()
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='courier', address=address,
                                    shipped_at=now, delivered_at=now - timedelta(days=2))

    def test_delivered_without_shipped(self, order, address):
        """
        Доставка без даты отправки
        Ожидаемый результат: ошибка при наличии delivered_at без shipped_at
        """
        with pytest.raises(IntegrityError):
            Delivery.objects.create(order=order, delivery_type='courier', address=address,
                                    delivered_at=timezone.now())

    def test_shipped_without_delivered(self, order, address):
        """
        Отправка без даты доставки
        Ожидаемый результат: допускается
        """
        now = timezone.now()
        delivery = Delivery.objects.create(order=order, delivery_type='courier', address=address,
                                           shipped_at=now, delivered_at=None)
        assert delivery.shipped_at == now and delivery.delivered_at is None

    def test_no_dates(self, order, address):
        """
        Доставка без дат
        Ожидаемый результат: допускается
        """
        delivery = Delivery.objects.create(order=order, delivery_type='courier', address=address)
        assert delivery.shipped_at is None and delivery.delivered_at is None