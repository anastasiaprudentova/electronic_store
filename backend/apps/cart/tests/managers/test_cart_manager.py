import pytest
from apps.cart.models import Cart

@pytest.mark.django_db
class TestCartManager:
    """Тестирование CartManager"""
    def test_total_price_user(self, user, variation):
        """
        Подсчет общей стоимости корзины
        Ожидаемый результат: сумма quantity * price для всех позиций
        """
        Cart.objects.create(user=user, variation=variation, quantity=2)
        assert Cart.objects.total_price_user(user) == 2 * variation.price

    def test_total_price_user_empty(self, user):
        """
        Подсчет стоимости пустой корзины
        Ожидаемый результат: возвращает 0
        """
        assert Cart.objects.total_price_user(user) == 0

    def test_items_count(self, user, variation):
        """
        Подсчет количества товаров
        Ожидаемый результат: сумма quantity всех позиций
        """
        Cart.objects.create(user=user, variation=variation, quantity=3)
        assert Cart.objects.items_count(user) == 3

    def test_items_count_empty(self, user):
        """
        Подсчет количества товаров в пустой корзине
        Ожидаемый результат: возвращает 0
        """
        assert Cart.objects.items_count(user) == 0

    def test_clear_cart(self, user, variation):
        """
        Очистка корзины с товарами
        Ожидаемый результат: все элементы удалены, возвращает количество удаленных
        """
        Cart.objects.create(user=user, variation=variation, quantity=2)
        assert Cart.objects.clear_cart(user) == 1
        assert Cart.objects.filter(user=user).count() == 0

    def test_clear_cart_empty(self, user):
        """
        Очистка пустой корзины
        Ожидаемый результат: возвращает 0
        """
        assert Cart.objects.clear_cart(user) == 0

    def test_add_item_new(self, user, variation):
        """
        Добавление нового товара
        Ожидаемый результат: создается запись с указанным количеством
        """
        item, created = Cart.objects.add_item(user, variation.id, quantity=2)
        assert created and item.quantity == 2

    def test_add_item_existing(self, user, variation):
        """
        Добавление существующего товара
        Ожидаемый результат: количество увеличивается
        """
        Cart.objects.add_item(user, variation.id, quantity=2)
        item, created = Cart.objects.add_item(user, variation.id, quantity=3)
        assert not created and item.quantity == 5

    def test_add_item_default(self, user, variation):
        """
        Добавление товара с количеством по умолчанию
        Ожидаемый результат: quantity = 1
        """
        item, created = Cart.objects.add_item(user, variation.id)
        assert created and item.quantity == 1

    def test_remove_item(self, user, variation):
        """
        Удаление товара из корзины
        Ожидаемый результат: товар удален, возвращает True
        """
        Cart.objects.add_item(user, variation.id)
        assert Cart.objects.remove_list(user, variation.id) is True
        assert Cart.objects.filter(user=user).count() == 0

    def test_remove_nonexistent(self, user, variation):
        """
        Удаление несуществующего товара
        Ожидаемый результат: возвращает False
        """
        assert Cart.objects.remove_list(user, variation.id) is False