import pytest
from apps.catalog.models import Product

@pytest.mark.django_db
class TestProductManager:
    def test_without_reviews_returns_products_with_no_reviews(self, product):
        """
        Ожидаемые результаты: метод возвращает товары без отзывов.
        """
        results = Product.objects.without_reviews()
        assert product in results

    def test_without_reviews_excludes_products_with_reviews(self, product, user, review):
        """
        Ожидаемые результаты: метод исключает товары с отзывами
        """
        results = Product.objects.without_reviews()
        assert product not in results

    def test_without_reviews_excludes_inactive(self, product):
        """
        Ожидаемые результаты: метод исключает неактивные товары
        """
        product.is_active = False
        product.save()

        results = Product.objects.without_reviews()
        assert product not in results