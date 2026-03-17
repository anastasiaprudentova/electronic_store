from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count, Sum
from django.db.models.functions import Coalesce

class OrderManager(models.Manager):
    """Менеджер для работы с заказами"""
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

    def last_days(self,days=7):
        """Заказы за последние N дней"""
        last_days = timezone.now().date() - timedelta(days=days)
        return self.filter(created_at__gte=last_days)

    def by_status(self,status):
        """Заказы с указанным статусом"""
        return self.filter(status=status)

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