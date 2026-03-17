from django.db import models
from apps.catalog.models import Product
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel

class Wishlist(TimeStampedModel):
    """Избранное пользователя"""
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'wishlist', verbose_name = 'Пользователь')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
        ]
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"