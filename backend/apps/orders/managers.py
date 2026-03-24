from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Sum


class OrderQuerySet(models.QuerySet):
    """Кастомный QuerySet для заказов с методами фильтрации"""

    def created_today(self):
        """Заказы, созданные сегодня"""
        today = timezone.now().date()
        return self.filter(created_at__date=today)

    def by_user(self, user):
        """Заказы конкретного пользователя"""
        return self.filter(user=user)

    def new(self):
        """Новые заказы (статус 'new')"""
        return self.filter(status='new')

    def paid(self):
        """Оплаченные заказы (статус 'paid')"""
        return self.filter(status='paid')

    def processing(self):
        """Заказы в обработке (статус 'processing')"""
        return self.filter(status='processing')

    def last_days(self, days=7):
        """Заказы за последние N дней"""
        last_days = timezone.now().date() - timedelta(days=days)
        return self.filter(created_at__gte=last_days)

    def by_status(self, status):
        """Заказы с указанным статусом"""
        return self.filter(status=status)

    def average_paid_order_value(self):
        """Средняя сумма оплаченных заказов (для QuerySet)"""
        result = self.filter(status='paid').aggregate(
            avg=Avg('total_amount')
        )
        return result['avg'] or 0

    def total_revenue(self):
        """Общая выручка по оплаченным заказам (для QuerySet)"""
        result = self.filter(status='paid').aggregate(
            total=Sum('total_amount')
        )
        return result['total'] or 0

class OrderManager(models.Manager):
    """Менеджер для работы с заказами"""

    def get_queryset(self):
        """Возвращает кастомный QuerySet"""
        return OrderQuerySet(self.model, using=self._db)

    def created_today(self):
        return self.get_queryset().created_today()

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def new(self):
        return self.get_queryset().new()

    def paid(self):
        return self.get_queryset().paid()

    def processing(self):
        return self.get_queryset().processing()

    def last_days(self, days=7):
        return self.get_queryset().last_days(days)

    def by_status(self, status):
        return self.get_queryset().by_status(status)

    def average_paid_order_value(self):
        """Средняя сумма оплаченных заказов"""
        result = self.filter(
            status='paid'
        ).aggregate(
            avg_count=Avg('total_amount')
        )
        return result['avg_count'] or 0

    def total_revenue(self):
        """Общая выручка по оплаченным заказам"""
        result = self.filter(
            status='paid'
        ).aggregate(
            total_revenue=Sum('total_amount')
        )
        return result['total_revenue'] or 0