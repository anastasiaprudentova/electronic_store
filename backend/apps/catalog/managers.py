from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Avg, Count

class ProductManager(models.Manager):
    """Менеджер для работы с товарами"""
    def in_stock(self):
        """Товары, которые есть в наличии"""
        return self.filter(
            variations__stocks__quantity__gt=0,
            is_active = True
        ).distinct()

    def new(self, days=30):
        """Товары, добавленные за последние N дней"""
        current_date = timezone.now() - timedelta(days=days)
        return self.filter(
            created_at__gte=current_date,
            is_active=True
        ).distinct()

    def search(self, query):
        """Поиск по названию"""
        if not query:
            return self.none()
        return self.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        ).distinct()

    def price_range(self, min_price=None, max_price=None):
        """Товары с ценой от min_price до max_price"""
        queryset = self.filter(is_active=True)
        if min_price is not None:
            queryset = queryset.filter(variations__price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(variations__price__lte=max_price)

        return queryset.distinct()

    def by_category(self, category_id):
        """Товары по категории"""
        return self.filter(
            category_id=category_id,
            is_active=True
        )

    def rating(self, min_rating=4):
        """Товары с рейтингом не ниже указанного"""
        return self.filter(
            is_active=True,
        ).annotate(
            avg=Avg('reviews__rating')
        ).filter(
            avg__gte=min_rating
        ).order_by("-avg")

    def by_brand(self, brand_id):
        """Товары указанного бренда"""
        return self.filter(
            brand_id=brand_id,
            is_active=True
        )

    def by_year(self, year):
        """Товары, созданные в указанном году"""
        return self.filter(
            created_at__year=year,
            is_active=True
        )

    def without_reviews(self):
        """Товары без отзывов"""
        return self.filter(
            is_active=True
        ).annotate(
            count = Count('reviews')
        ).filter(
            count = 0
        )

    def popular(self, min_orders=10):
        """Популярные товары (часто заказываемые)"""
        return self.filter(
            is_active=True,
        ).annotate(
            orders_count=Count('variations__order_items')
        ).filter(
            orders_count__gte=min_orders
        ).order_by('-orders_count')