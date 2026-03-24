import pytest
from django.db import IntegrityError
from apps.catalog.models import Brand

@pytest.mark.django_db
class TestBrandModel:
    """Тестирование модели Brand (бренды производителей)"""
    def test_create_brand_with_valid_name(self):
        """
        Создание бренда с валидным именем
        Ожидаемый результат: создание бренда, __str__ возвращает имя
        """
        brand = Brand.objects.create(name = "Samsung")
        assert brand.name == "Samsung"
        assert str(brand) == "Samsung"

    def test_create_brand_with_duplicate_name_raises_error(self):
        """
        Создание бренда с уже имеющимся именем
        Ожидаемый результат: возникновение ошибки уникальности
        """
        Brand.objects.create(name = "Samsung")
        with pytest.raises(IntegrityError):
            Brand.objects.create(name = "Samsung")

    def test_brand_ordering(self):
        """
        Сортировка брендов по умолчанию
        Ожидаемый результат: бренды сортируются по алфавиту
        """
        Brand.objects.create(name = "Samsung")
        Brand.objects.create(name = "Apple")
        Brand.objects.create(name = "Xiaomi")

        brands = Brand.objects.all()
        assert brands[0].name == "Apple"
        assert brands[1].name == "Samsung"
        assert brands[2].name == "Xiaomi"

    def test_brand_str_method(self):
        """
        Строковое представление бренда
        Ожидаемый результат: __str__ возвращает имя бренда
        """
        brand = Brand(name = "Samsung")
        assert str(brand) == "Samsung"