import pytest
from apps.catalog.models import Product
from apps.catalog.models import Brand

@pytest.mark.django_db
class TestProductManager:
    def test_by_brand_returns_products_of_brand(self, product, brand):
        """
        Ожидаемый результат: фильтр по бренду возвращает товары этого бренда
        """
        results = Product.objects.by_brand(brand.id)
        assert product in results

    def test_by_brand_excludes_other_brands(self, product, brand):
        """
        Ожидаемый результат: фильтр по бренду исключает товары других брендов
        """
        other_brand = Brand.objects.create(name="Apple")

        results = Product.objects.by_brand(other_brand.id)
        assert product not in results