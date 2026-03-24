import pytest
from apps.catalog.models import Product
from apps.catalog.models import Category

@pytest.mark.django_db
class TestProductManager:
    def test_by_category_returns_products_in_category(self, product, category):
        """
        Ожидаемый результат: фильтр по категории возвращает товары в этой категории.
        """
        results = Product.objects.by_category(category.id)
        assert product in results

    def test_by_category_excludes_other_categories(self, product, category):
        """
        Ожидаемый результат: фильтр по категории исключает товары из других категорий
        """
        other_category = Category.objects.create(name="Ноутбуки")

        results = Product.objects.by_category(other_category.id)
        assert product not in results

    def test_by_category_excludes_inactive(self, product, category):
        """
        Ожидаемый результат: фильтр по категории исключает неактивные товары
        """
        product.is_active = False
        product.save()

        results = Product.objects.by_category(category.id)
        assert product not in results