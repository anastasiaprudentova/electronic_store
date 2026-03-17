from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Avg, Count, Sum, F
from django.db.models.functions import Coalesce
from django.db.models import Value
from apps.catalog.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from .managers import ReviewManager

class Review(TimeStampedModel):
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
    is_moderated = models.BooleanField('Проверен модератором', default=False)

    objects=ReviewManager()

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