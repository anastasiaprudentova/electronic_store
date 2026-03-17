from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models import Q, Avg, Count, Sum, F
from django.db.models.functions import Coalesce
from apps.catalog.models import Product, Variation
from apps.core.models import TimeStampedModel

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

class Cart(TimeStampedModel):
    """Корзина пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'cart', verbose_name = 'Пользователь')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, verbose_name = 'Товар')
    quantity = models.IntegerField('Количество', default=1, validators = [MinValueValidator(1)])

    objects=CartManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        unique_together = ('user', 'variation')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['variation']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.variation.product.name} × {self.quantity}'

    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.variation.price * self.quantity