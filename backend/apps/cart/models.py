from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models import Q, Avg, Count, Sum, F
from django.db.models.functions import Coalesce
from apps.catalog.models import Product, Variation

class ReviewManager(models.Manager):
    """Менеджер для работы с отзывами"""
    def positive(self):
        """Положительные отзывы (рейтинг 4-5)"""
        return self.filter(
            rating__gte=4,
            is_moderated=True
        )

    def pending(self):
        """Отзывы, ожидающие проверки модератором"""
        return self.filter(
            is_moderated=False
        )

    def moderated(self):
        """Проверенные отзывы (прошедшие модерацию)"""
        return self.filter(
            is_moderated=True
        )

    def for_product(self, product):
        """Отзывы для конкретного товара"""
        return self.filter(
            product=product,
            is_moderated=True
        )

    def with_rating(self, rating):
        """Отзывы с конкретной оценкой"""
        return self.filter(
            rating=rating,
            is_moderated=True
        )

    def last_review(self,days = 7):
        """Отзывы за последние N дней"""
        result = timezone.now() - timedelta(days=days)
        return self.filter(
            created_at__gte=result,
            is_moderated=True
        )

    def today(self):
        """Отзывы, созданные сегодня"""
        today = timezone.now().date()
        return self.filter(
            created_at__gte=today,
            is_moderated=True
        )

    def average_rating(self, product = None):
        """Средний рейтинг (для конкретного товара или для всех)"""
        queryset = self.filter(is_moderated=True)
        if product:
            queryset = queryset.filter(product=product)
        return queryset.aggregate(
            avg=Coalesce(Avg('rating'), Value(0.0))
        )['avg']

    def total_count(self, product = None):
        """Общее количество отзывов"""
        queryset = self.filter(is_moderated=True)
        if product:
            queryset = queryset.filter(product=product)
        return queryset.count()

    def rating_distribution(self, product = None):
        """Распределение оценок (сколько отзывов с каждой оценкой)"""
        queryset = self.filter(is_moderated=True)
        if product:
            queryset = queryset.filter(product=product)

        distribution = queryset.values('rating').annotate(
            count=Count('id')
        ).order_by('rating')

        result = {1: 0, 2: 0, 3: 0, 4: 0, 5:0}
        for i in distribution:
            result [i['rating']] = i['count']

        return result

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

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'cart', verbose_name = 'Пользователь')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, verbose_name = 'Товар')
    quantity = models.IntegerField('Количество', default=1, validators = [MinValueValidator(1)])
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    objects=CartManager()
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

