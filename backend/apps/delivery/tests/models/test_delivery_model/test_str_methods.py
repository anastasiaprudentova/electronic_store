import pytest
from apps.delivery.models import Delivery

@pytest.mark.django_db
class TestDeliveryStrMethods:
    """Тесты строковых методов модели Delivery"""

    def test_str_method_courier(self, order, address):
        """
        Строковое представление для курьерской доставки
        Ожидаемый результат: __str__ возвращает "Курьер: {address}"
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='courier',
            address=address
        )
        expected = f"Курьер: {address}"
        assert str(delivery) == expected

    def test_str_method_pickup(self, order, pickup_point):
        """
        Строковое представление для доставки в ПВЗ
        Ожидаемый результат: __str__ возвращает "ПВЗ: {pickup_point.name}"
        """
        delivery = Delivery.objects.create(
            order=order,
            delivery_type='pickup',
            pickup_point=pickup_point
        )
        expected = f"ПВЗ: {pickup_point.name}"
        assert str(delivery) == expected