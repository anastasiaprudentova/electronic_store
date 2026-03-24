from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from apps.catalog.models import Variation
from apps.core.models import TimeStampedModel
from .managers import OrderManager


class PickupPoint(models.Model):
    """Пункты выдачи заказов"""
    name = models.CharField('Название', max_length=255)
    carrier = models.CharField('Служба доставки', max_length=100)
    city = models.CharField('Город', max_length=100)
    address = models.CharField('Адрес', max_length=255)
    working_hours = models.TextField('Режим работы', blank = True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'
        ordering = ['-is_active', 'city']
        indexes = [
            models.Index(fields=['carrier']),
            models.Index(fields=['city'])
        ]

    def __str__(self):
        return f"{self.name} ({self.city})"

class Order(TimeStampedModel):
    """Заказы"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', verbose_name = 'Пользователь')
    address = models.ForeignKey('users.Address', on_delete=models.PROTECT, related_name = 'orders', verbose_name = 'Адрес доставки')
    order_number = models.CharField('Номер заказа', max_length=50, unique=True, validators=[RegexValidator(regex=r'^[A-Z0-9-]+$',
            message='Номер заказа может содержать только заглавные буквы, цифры и дефис')])
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField('Сумма заказа', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    comment = models.TextField('Комментарий к заказу', blank = True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural ='Заказы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Заказ №{self.order_number}"

class OrderItem(models.Model):
    """Состав заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    variation = models.ForeignKey(Variation, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField('Итоговая цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['variation']),
        ]

    def __str__(self):
        return f"{self.variation.product.name} x{self.quantity}"