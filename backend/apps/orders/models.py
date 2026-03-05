from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from apps.users.models import Address
from apps.catalog.models import Variation
from django.db.models import Q, F

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

class Order(models.Model):
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
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

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