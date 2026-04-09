import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.orders.models import OrderItem

@pytest.mark.django_db
class TestOrderItemModel:
    """Тестирование модели OrderItem (позиции заказа)"""

    def test_create_order_item_with_valid_data(self, order, variation):
        """
        Создание позиции заказа с валидными данными
        Ожидаемый результат: позиция создается со всеми полями
        """
        item = OrderItem.objects.create(
            order=order,
            variation=variation,
            quantity=3,
            price_per_unit=80000,
            total_price=240000
        )

        assert item.order == order
        assert item.variation == variation
        assert item.quantity == 3
        assert item.price_per_unit == 80000
        assert item.total_price == 240000

    def test_order_item_quantity_validation(self, order, variation):
        """
        Валидация количества
        Ожидаемый результат: количество должно быть >= 1
        """
        with pytest.raises(ValidationError):
            item = OrderItem(
                order=order,
                variation=variation,
                quantity=0,
                price_per_unit=80000,
                total_price=0
            )
            item.full_clean()

    def test_order_item_price_validation(self, order, variation):
        """
        Валидация цены
        Ожидаемый результат: цена не может быть отрицательной
        """
        with pytest.raises(ValidationError):
            item = OrderItem(
                order=order,
                variation=variation,
                quantity=1,
                price_per_unit=-1000,
                total_price=-1000
            )
            item.full_clean()

    def test_order_item_total_price_calculation(self, order, variation):
        """
        Проверка итоговой цены
        Ожидаемый результат: total_price = quantity * price_per_unit
        """
        quantity = 3
        price = 80000
        total = quantity * price

        item = OrderItem.objects.create(
            order=order,
            variation=variation,
            quantity=quantity,
            price_per_unit=price,
            total_price=total
        )
        assert item.total_price == quantity * price

    def test_order_item_str_method(self, order_item, variation):
        """
        Строковое представление позиции заказа
        Ожидаемый результат: __str__ возвращает "Название товара x{quantity}"
        """
        expected = f"{variation.product.name} x{order_item.quantity}"
        assert str(order_item) == expected

    def test_order_item_on_delete_protect_variation(self, order, variation):
        """
        Защита от удаления вариации, используемой в заказах
        Ожидаемый результат: нельзя удалить вариацию, на которую есть ссылки в заказах
        """
        OrderItem.objects.create(
            order=order,
            variation=variation,
            quantity=1,
            price_per_unit=80000,
            total_price=80000
        )

        with pytest.raises(IntegrityError):
            variation.delete()

    def test_order_item_cascade_delete_with_order(self, order, variation):
        """
        Каскадное удаление при удалении заказа
        Ожидаемый результат: при удалении заказа удаляются все его позиции
        """
        OrderItem.objects.create(
            order=order,
            variation=variation,
            quantity=1,
            price_per_unit=80000,
            total_price=80000
        )

        order_id = order.id
        order.delete()

        assert OrderItem.objects.filter(order_id=order_id).count() == 0