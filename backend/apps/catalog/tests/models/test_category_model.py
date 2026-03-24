import pytest
from django.db import IntegrityError
from apps.catalog.models import Category

@pytest.mark.django_db
class TestCategoryModel:
    """Тестирование модели Category (категории товаров)"""
    def test_create_category_with_valid_name(self):
        """
        Создание категории с валидным именем
        Ожидаемый результат: создание category, __str__ возвращает имя
        """
        category = Category.objects.create(name = "Смартфоны")
        assert category.name == "Смартфоны"

    def test_create_category_with_parent(self):
        """
        Создание подкатегорий с родительской категорией
        Ожидаемый результат: parent ссылается на родителя
        """
        parent = Category.objects.create(name = "Электроника")
        child = Category.objects.create(name = "Смартфоны", parent = parent)

        assert child.parent == parent
        assert child in parent.children.all()

    def test_category_unique_name(self):
        """
        Создание категории с уже имеющимся именем
        Ожидаемый результат: возникновение ошибки уникальности
        """
        Category.objects.create(name="Смартфоны")
        with pytest.raises(IntegrityError):
            Category.objects.create (name="Смартфоны")

    def test_category_str_method(self):
        """
        Строковое представление категории
        Ожидаемый результат: __str__ возвращает имя категории
        """
        category = Category(name="Ноутбуки")
        assert str(category) == "Ноутбуки"

    def test_category_ordering(self):
        """
        Сортировка категорий по умолчанию
        Ожидаемый результат: категории сортируются по алфавиту
        """
        Category.objects.create(name = 'Ноутбуки')
        Category.objects.create(name = 'Смартфоны')
        Category.objects.create(name = 'Аксессуары')

        categories = Category.objects.all()
        assert categories[0].name == 'Аксессуары'
        assert categories[1].name == 'Ноутбуки'
        assert categories[2].name == 'Смартфоны'