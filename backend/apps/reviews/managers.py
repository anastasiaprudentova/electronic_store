from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.db.models import Value

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