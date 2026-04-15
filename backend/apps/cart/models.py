from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from apps.catalog.models import Variation
from apps.core.models import TimeStampedModel
from .managers import CartManager

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