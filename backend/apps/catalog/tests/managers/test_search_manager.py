import pytest
from apps.catalog.models import Product

@pytest.mark.django_db
class TestProductManager:
    def test_search_finds_product_by_name(self, product):
        """
        Ожидаемый результат: поиск находит товар по названию.
        """
        results = Product.objects.search("Galaxy")
        assert product in results

    def test_search_finds_product_by_description(self, product):
        """
        Ожидаемый результат: поиск находит товар по описанию.
        """
        results = Product.objects.search("смартфон")
        assert product in results

    def test_search_is_case_insensitive(self, product):
        """
        Ожидаемый результат: поиск не зависит от регистра.
        """
        results = Product.objects.search("galaxy")
        assert product in results

        results = Product.objects.search("GALAXY")
        assert product in results

    def test_search_returns_empty_for_empty_query(self, product):
        """
        Ожидаемый результат: при пустом запросе возвращается пустой QuerySet.
        """
        results = Product.objects.search("")
        assert results.count() == 0
        assert results.exists() is False

    def test_search_returns_empty_for_no_matches(self, product):
        """
        Ожидаемый результат: при отсутствии совпадений возвращается пустой QuerySet.
        """
        results = Product.objects.search("отсутствующийзапрос")
        assert results.count() == 0

    def test_search_excludes_inactive_products(self, product):
        """
        Ожидаемый результат: поиск исключает неактивные товары.
        """
        product.is_active = False
        product.save()

        results = Product.objects.search("Galaxy")
        assert product not in results