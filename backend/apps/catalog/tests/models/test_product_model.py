import pytest
from apps.catalog.models import Product

@pytest.mark.django_db
class TestProductModel:
    """Тестирование модели Product (товары)"""
    def test_create_product_with_valid_data(self,brand,category):
        """
        Создание товара с валидными данными
        Ожидаемый результат: товар создается со всеми полями.
        """
        product = Product.objects.create(
            name = "iPhone 14",
            brand = brand,
            category = category,
            description = "Флагманский смартфон Apple"
        )

        assert product.name == "iPhone 14"
        assert product.brand == brand
        assert product.category == category
        assert product.description == "Флагманский смартфон Apple"
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None

    def test_product_str_method(self,product):
        """
        Строковое представление товара
        Ожидаемый результат: __str__ возвращает название товара.
        """
        assert str(product) == product.name

    def test_product_ordering(self,brand,category):
        """
        Сортировка товаров по умолчанию (новые сверху)
        Ожидаемый результат: товары сортируются по убыванию даты создания
        """
        p1 = Product.objects.create(name = "Старый", brand=brand, category = category)
        p2 = Product.objects.create(name = "Новый", brand = brand, category = category)

        products = Product.objects.all()
        assert products[0] == p2
        assert products[1] == p1