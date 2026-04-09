import pytest
from apps.catalog.models import Product, Variation, Stock

@pytest.mark.django_db
class TestProductManager:
    """Тестирование ProductManager"""
    def test_in_stock_returns_products_with_positive_stock(self, product, variation):
        """
        Ожидаемый результат: метод in_stock() возвращает товары, у которых есть остатки > 0.
        """
        Stock.objects.create(variation=variation, quantity=5, reserved=0)
        in_stock = Product.objects.in_stock()
        assert product in in_stock
        assert in_stock.count() == 1

    def test_in_stock_excludes_products_with_zero_stock(self,product, variation):
        """
        Ожидаемый результат: метод in_stock() исключает товары с нулевым остатком.
        """
        Stock.objects.create(variation=variation, quantity=0, reserved=0)
        in_stock = Product.objects.in_stock()
        assert product not in in_stock

    def test_in_stock_excludes_inactive_products(self,product,variation):
        """
        Ожидаемый результат: метод in_stock() исключает неактивные товары.
        """
        Stock.objects.create(variation=variation, quantity=5, reserved=0)
        product.is_active = False
        product.save()

        in_stock = Product.objects.in_stock()
        assert product not in in_stock

    def test_in_stock_returns_distinct_products(self,product, variation):
        """
        Ожидаемый результат: метод in_stock() возвращает уникальные товары
        """
        Variation.objects.create(product=product, sku="VAR2", price=100)
        Stock.objects.create(variation=variation, quantity=5)

        in_stock = Product.objects.in_stock()
        assert in_stock.count() == 1