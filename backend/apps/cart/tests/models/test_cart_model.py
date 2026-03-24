import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.cart.models import Cart
from apps.catalog.models import Variation
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestCartModel:
    """Тестирование модели Cart (корзина пользователя)"""

    def test_create_cart_with_valid_data(self, user, variation):
        """
        Создание элемента корзины с валидными данными
        Ожидаемый результат: элемент создается со всеми полями
        """
        cart = Cart.objects.create(
            user=user,
            variation=variation,
            quantity=3
        )
        assert cart.user == user
        assert cart.variation == variation
        assert cart.quantity == 3
        assert cart.created_at is not None
        assert cart.updated_at is not None

    def test_cart_quantity_validation(self, user, variation):
        """
        Валидация количества
        Ожидаемый результат: количество должно быть >= 1
        """
        with pytest.raises(ValidationError):
            cart = Cart(user=user, variation=variation, quantity=0)
            cart.full_clean()

    def test_cart_unique_user_variation(self, user, variation):
        """
        Уникальность пары пользователь-вариация
        Ожидаемый результат: один пользователь может добавить вариацию в корзину только один раз
        """
        Cart.objects.create(user=user, variation=variation, quantity=2)
        with pytest.raises(IntegrityError):
            Cart.objects.create(user=user, variation=variation, quantity=3)

    def test_cart_str_method(self, cart_item):
        """
        Строковое представление элемента корзины
        Ожидаемый результат: "username - product name × quantity"
        """
        expected = f"{cart_item.user.username} - {cart_item.variation.product.name} × {cart_item.quantity}"
        assert str(cart_item) == expected

    def test_cart_total_price_property(self, cart_item):
        """
        Свойство total_price
        Ожидаемый результат: возвращает quantity * price
        """
        assert cart_item.total_price == cart_item.quantity * cart_item.variation.price

    def test_cart_belongs_to_user(self, user, variation):
        """
        Принадлежность корзины пользователю
        Ожидаемый результат: корзины разных пользователей не перемешиваются
        """
        other_user = User.objects.create_user(username="other", password="123")

        cart1 = Cart.objects.create(user=user, variation=variation, quantity=1)
        cart2 = Cart.objects.create(user=other_user, variation=variation, quantity=2)

        assert cart1.user == user
        assert cart2.user == other_user
        assert Cart.objects.filter(user=user).count() == 1
        assert Cart.objects.filter(user=other_user).count() == 1

    def test_cart_on_delete_cascade_user(self, user, variation):
        """
        Каскадное удаление при удалении пользователя
        Ожидаемый результат: при удалении пользователя удаляются все его корзины
        """
        Cart.objects.create(user=user, variation=variation, quantity=1)
        user_id = user.id
        user.delete()
        assert Cart.objects.filter(user_id=user_id).count() == 0

    def test_cart_user_can_have_multiple_items(self, user, variation, product):
        """
        Пользователь может иметь несколько товаров в корзине
        Ожидаемый результат: ограничений на количество нет
        """
        variation2 = Variation.objects.create(
            product=product,
            sku="S24-WHT-256",
            price=80000
        )

        Cart.objects.create(user=user, variation=variation, quantity=1)
        Cart.objects.create(user=user, variation=variation2, quantity=2)

        assert Cart.objects.filter(user=user).count() == 2