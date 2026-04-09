import pytest
from django.db import IntegrityError
from apps.catalog.models import Stock

@pytest.mark.django_db
class TestStockModel:
    """Тестирование модели Stock (остатки на складах)"""
    def test_create_stock_with_valid_data(self, variation):
        """
        Создание остатка с валидными данными
        Ожидаемый результат: остаток создается со всеми полями
        """
        stock = Stock.objects.create(
            variation=variation,
            warehouse_id=1,
            quantity=10,
            reserved=2
        )

        assert stock.variation == variation
        assert stock.warehouse_id == 1
        assert stock.quantity == 10
        assert stock.reserved == 2

    def test_stock_unique_variation_warehouse(self, variation):
        """
        Уникальность пары вариация-склад
        Ожидаемый результат: нельзя создать две записи для одной вариации на одном складе
        """
        Stock.objects.create(variation=variation, warehouse_id=1, quantity=10)
        with pytest.raises(IntegrityError):
            Stock.objects.create(variation=variation, warehouse_id=1, quantity=5)

    def test_stock_reserved_cannot_exceed_quantity(self, variation):
        """
        Ограничение: резерв не может превышать количество
        Ожидаемый результат: при попытке создать запись с reserved > quantity возникает ошибка
        """
        with pytest.raises(Exception):
            Stock.objects.create(variation=variation, warehouse_id=1, quantity=5, reserved=10)

    def test_stock_available_property(self, variation):
        """
        Свойство available (доступное количество)
        Ожидаемый результат: available = quantity - reserved
        """
        stock = Stock.objects.create(
            variation=variation,
            warehouse_id=1,
            quantity=10,
            reserved=3
        )
        assert stock.available == 7

    def test_stock_available_with_no_reserved(self, variation):
        """
        Свойство available при отсутствии резерва
        Ожидаемый результат: available = quantity
        """
        stock = Stock.objects.create(
            variation=variation,
            warehouse_id=1,
            quantity=10,
            reserved=0
        )
        assert stock.available == 10

    def test_stock_str_method(self, stock):
        """
        Строковое представление остатка
        Ожидаемый результат: __str__ возвращает "Артикул - склад N: количество шт"
        """
        expected = f"{stock.variation.sku} - склад {stock.warehouse_id}: {stock.quantity} шт"
        assert str(stock) == expected