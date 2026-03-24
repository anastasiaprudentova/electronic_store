import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.catalog.models import Variation

@pytest.mark.django_db
class TestVariationModel:
    """Тестирование модели Variation (вариации товаров)"""
    def test_create_variation_with_valid_data(self,product):
        """
        Создание вариации с валидными данными
        Ожидаемый результат: вариация создается со всеми полями
        """
        variation = Variation.objects.create(
            product = product,
            sku="IP14-BLK-128",
            price=80000,
            is_active=True
        )

        assert variation.product == product
        assert variation.sku == "IP14-BLK-128"
        assert variation.price == 80000
        assert variation.is_active is True

    def test_variation_unique_sku(self,product):
        """
        Уникальность артикула
        Ожидаемый результат: при создании дубликата возникает ошибка
        """
        Variation.objects.create(
            product = product,
            sku="IP14-BLK-128",
            price=80000,
        )
        with pytest.raises(IntegrityError):
            Variation.objects.create(
                product = product,
                sku="IP14-BLK-128",
                price=80000,
            )

    def test_variation_price_non_negative(self, product):
        """
        Проверка отрицательной цены
        Ожидаемый результат: при отрицательной цене возникает ошибка
        """
        with pytest.raises(ValidationError):
            variation = Variation(
                product=product,
                sku="IP14-BLK-128",
                price=-1000,
            )
            variation.full_clean()

    def test_variation_str_method(self,variation):
        """
        Строковое представление вариации
        Ожидаемый результат: __str__ возвращает "Название товара - Артикул"
        """
        expected = f"{variation.product.name} - {variation.sku}"
        assert str(variation) == expected