import pytest
from apps.catalog.models import Product, Variation

@pytest.mark.django_db
class TestProductManager:
    def test_price_range_with_min_and_max(self, product, variation):
        """
        Ожидаемый результат: фильтр по диапазону цен с min и max.
        """
        variation.price = 5000
        variation.save()

        results = Product.objects.price_range(min_price=1000, max_price=10000)
        assert product in results

    def test_price_range_with_min_only(self, product, variation):
        """
        Ожидаемый результат: фильтр только с минимальной ценой.
        """
        variation.price = 5000
        variation.save()

        results = Product.objects.price_range(min_price=1000)
        assert product in results

        results = Product.objects.price_range(min_price=10000)
        assert product not in results

    def test_price_range_with_max_only(self, product, variation):
        """
        Ожидаемый результат: фильтр только с максимальной ценой.
        """
        variation.price = 5000
        variation.save()

        results = Product.objects.price_range(max_price=10000)
        assert product in results

        results = Product.objects.price_range(max_price=1000)
        assert product not in results

    def test_price_range_returns_distinct(self, product, variation):
        """
        Ожидаемый результат: price_range возвращает уникальные товары
        """
        Variation.objects.create(product=product, sku="VAR2", price=4000)

        results = Product.objects.price_range(min_price=1000, max_price=90000)
        assert results.count() == 1

    def test_price_range_excludes_inactive(self, product, variation):
        """
        Ожидаемый результат: price_range исключает неактивные товары
        """
        variation.price = 5000
        variation.save()
        product.is_active = False
        product.save()

        results = Product.objects.price_range(min_price=1000, max_price=10000)
        assert product not in results