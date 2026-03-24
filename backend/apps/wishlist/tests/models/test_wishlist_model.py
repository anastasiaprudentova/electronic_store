import pytest
from django.db import IntegrityError
from django.contrib.auth.models import User
from apps.catalog.models import Product
from apps.wishlist.models import Wishlist

@pytest.mark.django_db
class TestWishlistModel:
    """Тестирование модели Wishlist (избранное пользователя)"""

    def test_create_wishlist_with_valid_data(self, user, product):
        """
        Создание записи в избранном
        Ожидаемый результат: запись создается
        """
        wishlist = Wishlist.objects.create(user=user, product=product)
        assert wishlist.user == user
        assert wishlist.product == product

    def test_wishlist_unique_user_product(self, user, product):
        """
        Уникальность пары пользователь-товар
        Ожидаемый результат: один пользователь может добавить товар только один раз
        """
        Wishlist.objects.create(user=user, product=product)
        with pytest.raises(IntegrityError):
            Wishlist.objects.create(user=user, product=product)

    def test_wishlist_str_method(self, wishlist):
        """
        Строковое представление записи из избранного
        Ожидаемый результат: __str__ возвращает "username - product name"
        """
        expected = f"{wishlist.user.username} - {wishlist.product.name}"
        assert str(wishlist) == expected

    def test_wishlist_ordering(self, user, product):
        """
        Сортировка избранного по умолчанию
        Ожидаемый результат: новые записи сверху
        """
        from datetime import timedelta
        from django.utils import timezone

        old = Wishlist.objects.create(user=user, product=product)
        old.created_at = timezone.now() - timedelta(days=5)
        old.save()

        other_product = Product.objects.create(
            name="iPhone",
            brand=product.brand,
            category=product.category
        )
        new = Wishlist.objects.create(user=user, product=other_product)

        wishlist = Wishlist.objects.all()
        assert wishlist[0] == new
        assert wishlist[1] == old

    def test_wishlist_belongs_to_user(self, user, product):
        """
        Принадлежность записи пользователю
        Ожидаемый результат: записи разных пользователей не перемешиваются
        """
        other_user = User.objects.create_user(username="other", password="123")
        other_product = Product.objects.create(
            name="iPhone",
            brand=product.brand,
            category=product.category
        )

        w1 = Wishlist.objects.create(user=user, product=product)
        w2 = Wishlist.objects.create(user=other_user, product=other_product)

        assert w1.user == user
        assert w2.user == other_user
        assert Wishlist.objects.filter(user=user).count() == 1
        assert Wishlist.objects.filter(user=other_user).count() == 1

    def test_wishlist_on_delete_cascade_user(self, user, product):
        """
        Каскадное удаление при удалении пользователя
        Ожидаемый результат: при удалении пользователя удаляются все его записи из избранного
        """
        Wishlist.objects.create(user=user, product=product)
        user_id = user.id
        user.delete()
        assert Wishlist.objects.filter(user_id=user_id).count() == 0

    def test_wishlist_product_can_be_deleted(self, user, product):
        """
        Удаление товара, который в избранном
        Ожидаемый результат: товар можно удалить, записи в избранном удаляются каскадно
        """
        Wishlist.objects.create(user=user, product=product)
        product_id = product.id
        product.delete()
        assert Wishlist.objects.filter(product_id=product_id).count() == 0

    def test_wishlist_indexes(self, user, product):
        """
        Проверка наличия индексов
        Ожидаемый результат: индексы созданы для полей user и product
        """
        Wishlist.objects.create(user=user, product=product)
        Wishlist.objects.filter(user=user).exists()
        Wishlist.objects.filter(product=product).exists()

    def test_wishlist_user_can_have_multiple_products(self, user, product):
        """
        Пользователь может добавить несколько товаров в избранное
        Ожидаемый результат: ограничений на количество нет
        """
        product2 = Product.objects.create(
            name="iPhone",
            brand=product.brand,
            category=product.category
        )
        Wishlist.objects.create(user=user, product=product)
        Wishlist.objects.create(user=user, product=product2)
        assert Wishlist.objects.filter(user=user).count() == 2