from django.db import models
from django.core.validators import MinValueValidator
from apps.orders.models import Order

class Payment(models.Model):
    """Платежи по заказам"""
    METHOD_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершён'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='payment', verbose_name='Заказ')
    method = models.CharField('Способ оплаты', max_length=20, choices=METHOD_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField('ID транзакции', max_length=255, blank=True)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    paid_at = models.DateTimeField('Дата оплаты', null=True, blank=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"Платёж для {self.order.order_number}"