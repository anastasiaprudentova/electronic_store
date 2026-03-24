from django.db import models
from django.db.models import Sum, F

class CartManager(models.Manager):
    """Менеджер для работы с корзиной"""
    def total_price_user(self, user):
        """Общая стоимость корзины пользователя"""
        result = self.filter(
            user = user
        ).aggregate(
            total = Sum(F('quantity') * F('variation__price'))
        )
        return result['total'] or 0

    def items_count(self, user):
        """Количество товаров в корзине"""
        result = self.filter(
            user=user
        ).aggregate(
            total=Sum('quantity')
        )
        return result['total'] or 0

    def clear_cart(self,user):
        """Очистить корзину пользователя"""
        deleted_count, _ = self.filter(
            user=user
        ).delete()
        return deleted_count

    def add_item(self, user,variation_id, quantity=1):
        """Добавить товар в корзину (или увеличить количество)"""
        cart_item, created = self.get_or_create(
            user=user,
            variation_id=variation_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item, created

    def remove_list(self,user,variation_id):
        """Удалить товар из корзины"""
        deleted_count, _ = self.filter(
            user=user,
            variation_id=variation_id
        ).delete()
        return deleted_count>0