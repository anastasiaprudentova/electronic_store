import pytest
from datetime import timedelta
from django.utils import timezone
from apps.catalog.models import Product

@pytest.mark.django_db
class TestProductManager:
    def test_get_new_product_returns_products_created_in_last_n_days(self, product):
        """
        Ожидаемый результат: метод get_new_product() возвращает товары, созданные за последние N дней.
        """
        product.created_at = timezone.now() - timedelta(days=15)
        product.save()

        new_products = Product.objects.get_new_product(days=30)
        assert product in new_products

    def test_get_new_product_excludes_older_products(self, product):
        """
        Ожидаемый результат: метод get_new_product() исключает товары старше N дней.
        """
        product.created_at = timezone.now() - timedelta(days=60)
        product.save()

        new_products = Product.objects.get_new_product(days=30)
        assert product not in new_products

    def test_get_new_product_excludes_inactive_products(self, product):
        """
        Ожидаемый результат: метод get_new_product() исключает неактивные товары.
        """
        product.created_at = timezone.now() - timedelta(days=15)
        product.is_active = False
        product.save()

        new_products = Product.objects.get_new_product(days=30)
        assert product not in new_products

    def test_get_new_product_with_custom_days_parameter(self, product):
        """
        Ожидаемый результат: метод get_new_product() работает с кастомным значением days.
        """
        product.created_at = timezone.now() - timedelta(days=5)
        product.save()

        assert product in Product.objects.get_new_product(days=7)
        assert product not in Product.objects.get_new_product(days=3)