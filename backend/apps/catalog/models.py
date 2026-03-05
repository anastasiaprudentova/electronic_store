from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from apps.cart.models import Product, Variation
from django.db.models import Q

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'cart', verbose_name = 'Пользователь')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, verbose_name = 'Товар')
    quantity = models.IntegerField('Количество', default=1,
                                   validators = [MinValueValidator(1)])
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
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

class Wishlist(models.Model):
    """Избранное пользователя"""
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'wishlist', verbose_name = 'Пользователь')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

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


class Review(models.Model):
    """Отзывы на товары"""

    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'reviews', verbose_name = 'Пользователь' )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'reviews', verbose_name = 'Товар')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES, validators = [MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField('Комментарий', blank = True, null = True)
    advantages = models.TextField('Достоинства', blank=True)
    disadvantages = models.TextField('Недостатки', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_moderated = models.BooleanField('Проверен модератором', default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields = ['user']),
            models.Index(fields = ['product']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'

    @property
    def rating_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

