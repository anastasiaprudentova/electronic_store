import pytest
from django.utils import timezone
from apps.delivery.models import Delivery

@pytest.mark.django_db
class TestDeliveryStatus:
    """Тесты изменения статусов доставки"""

    def test_status_initial_state(self, order, address):
        """
        Начальный статус доставки
        Ожидаемый результат: по умолчанию статус 'pending'
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address
        )
        assert delivery.status == 'pending'

    def test_status_transition_pending_to_shipped(self, order, address):
        """
        Переход статуса из 'pending' в 'shipped'
        Ожидаемый результат: статус меняется, дата отправки устанавливается
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address,
            status='pending'
        )

        delivery.status = 'shipped'
        delivery.shipped_at = timezone.now()
        delivery.save()

        updated = Delivery.objects.get(id=delivery.id)
        assert updated.status == 'shipped'
        assert updated.shipped_at is not None

    def test_status_transition_shipped_to_delivered(self, order, address):
        """
        Переход статуса из 'shipped' в 'delivered'
        Ожидаемый результат: статус меняется, дата доставки устанавливается
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address,
            status='shipped',
            shipped_at=timezone.now()
        )

        delivery.status = 'delivered'
        delivery.delivered_at = timezone.now()
        delivery.save()

        updated = Delivery.objects.get(id=delivery.id)
        assert updated.status == 'delivered'
        assert updated.delivered_at is not None

    def test_status_choices(self, order, address):
        """
        Проверка допустимых статусов
        Ожидаемый результат: можно установить любой из допустимых статусов
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address
        )

        valid_statuses = ['pending', 'shipped', 'delivered']
        for status in valid_statuses:
            delivery.status = status
            delivery.save()
            assert Delivery.objects.get(id=delivery.id).status == status