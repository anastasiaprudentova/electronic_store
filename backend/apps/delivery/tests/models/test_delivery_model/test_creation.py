import pytest
from django.db import IntegrityError
from django.utils import timezone
from apps.delivery.models import Delivery

@pytest.mark.django_db
class TestDeliveryCreation:
    """Тесты создания доставки"""

    def test_create_courier_delivery_with_valid_data(self, order, address):
        """
        Создание курьерской доставки с валидными данными
        Ожидаемый результат: доставка создается со всеми полями
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address,
            tracking_number='TRACK123',
            carrier='СДЭК',
            status='pending'
        )

        assert delivery.order == order
        assert delivery.delivery_type == 'courier'
        assert delivery.address == address
        assert delivery.pickup_point is None
        assert delivery.tracking_number == 'TRACK123'
        assert delivery.carrier == 'СДЭК'
        assert delivery.status == 'pending'
        assert delivery.shipped_at is None
        assert delivery.delivered_at is None

    def test_create_pickup_delivery_with_valid_data(self, order, pickup_point):
        """
        Создание доставки в ПВЗ с валидными данными
        Ожидаемый результат: доставка создается со всеми полями
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='pickup',
            pickup_point=pickup_point,
            tracking_number='TRACK456',
            carrier='Почта России',
            status='shipped',
            shipped_at=timezone.now()
        )

        assert delivery.order == order
        assert delivery.delivery_type == 'pickup'
        assert delivery.pickup_point == pickup_point
        assert delivery.address is None
        assert delivery.tracking_number == 'TRACK456'
        assert delivery.carrier == 'Почта России'
        assert delivery.status == 'shipped'
        assert delivery.shipped_at is not None

    def test_create_delivery_without_optional_fields(self, order, address):
        """
        Создание доставки без необязательных полей
        Ожидаемый результат: доставка создается с пустыми полями
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address
        )
        assert delivery.tracking_number == ""
        assert delivery.carrier == ""

    def test_delivery_unique_order(self, order, address):
        """
        Уникальность заказа (OneToOneField)
        Ожидаемый результат: нельзя создать две доставки для одного заказа
        """
        Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address
        )

        with pytest.raises(IntegrityError):
            Delivery.objects.create(
                order=order,
                delivery_type='pickup',
                address=address
            )