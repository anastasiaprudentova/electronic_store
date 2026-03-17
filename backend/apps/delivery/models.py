from django.db import models
from django.db.models import Q, F
from apps.orders.models import Order, PickupPoint

class Delivery(models.Model):
    """Доставка заказа"""
    DELIVERY_TYPES = [
        ('courier', 'Курьер'),
        ('pickup', 'Пункт выдачи'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='delivery', verbose_name='Заказ')
    delivery_type = models.CharField('Тип доставки', max_length=20, choices=DELIVERY_TYPES)

    # Для курьера
    address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Адрес доставки')

    # Для ПВЗ
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пункт выдачи')

    tracking_number = models.CharField('Трек-номер', max_length=255, blank=True)
    carrier = models.CharField('Служба доставки', max_length=100, blank=True)
    status = models.CharField('Статус доставки', max_length=20, choices=STATUS_CHOICES, default='pending')
    shipped_at = models.DateTimeField('Дата отправки', null=True, blank=True)
    delivered_at = models.DateTimeField('Дата доставки', null=True, blank=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['address']),
            models.Index(fields=['pickup_point']),
            models.Index(fields=['tracking_number']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    (models.Q(delivery_type='courier') &
                     models.Q(address__isnull=False) &
                     models.Q(pickup_point__isnull=True)) |
                    (models.Q(delivery_type='pickup') &
                     models.Q(address__isnull=True) &
                     models.Q(pickup_point__isnull=False))
                ),
                name='valid_delivery_type_fields'
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(delivered_at__isnull=True) |
                    models.Q(shipped_at__isnull=False, delivered_at__gte=models.F('shipped_at'))
                ),
                name='delivered_at_gte_shipped_at'
            )
        ]

    def __str__(self):
        if self.delivery_type == 'courier' and self.address:
            return f"Курьер: {self.address}"
        elif self.delivery_type == 'pickup' and self.pickup_point:
            return f"ПВЗ: {self.pickup_point.name}"
        return f"Доставка для заказа {self.order.order_number}"