from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
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
        ).order_by('-count')

class Brand(models.Model):
    """Бренды производителей"""
    name = models.CharField('Название', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Category(models.Model):
    """Категории товаров"""
    name = models.CharField('Название', max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товары"""
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд',
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )
    name = models.CharField('Название', max_length=255, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """Справочник характеристик"""
    ATTRIBUTE_TYPES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('boolean', 'Да/Нет'),
    ]

    name = models.CharField('Название', max_length=255, unique=True)
    type = models.CharField('Тип', max_length=20, choices=ATTRIBUTE_TYPES)
    unit = models.CharField('Единица измерения', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['type'])
        ]

    def __str__(self):
        if self.unit:
            return f'{self.name} ({self.unit})'
        return self.name


class AttributeValue(models.Model):
    """Значения характеристик для товаров"""
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name='Характеристика',
        related_name = 'values'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name = 'attribute_values'
    )

    text_value = models.CharField('Текстовое значение', max_length=255, blank=True, null=True)
    number_value = models.DecimalField(
        'Числовое значение',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    boolean_value = models.BooleanField('Логическое значение', blank=True, null=True)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'
        unique_together = ('attribute', 'product')

        indexes = [
            models.Index(fields=['attribute']),
            models.Index(fields=['product']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                        (models.Q(text_value__isnull=False) &
                         models.Q(number_value__isnull=True) &
                         models.Q(boolean_value__isnull=True)) |
                        (models.Q(text_value__isnull=True) &
                         models.Q(number_value__isnull=False) &
                         models.Q(boolean_value__isnull=True)) |
                        (models.Q(text_value__isnull=True) &
                         models.Q(number_value__isnull=True) &
                         models.Q(boolean_value__isnull=False))
                ),
                name='only_one_value_field_filled'
            )
        ]

    def __str__(self):
        if self.text_value:
            return f'{self.attribute.name}: {self.text_value}'
        elif self.number_value:
            unit = self.attribute.unit or ''
            if self.number_value == self.number_value // 1:
                return f'{self.attribute.name}: {self.number_value}'
            return f'{self.attribute.name}: {self.number_value} {unit}'
        elif self.boolean_value is not None:
            return f"{self.attribute.name}: {'Да' if self.boolean_value else 'Нет'}"
        return f'{self.attribute.name}: (незаполнено)'

class Variation(models.Model):
    """Вариации товаров (цвет, размер, комплектация)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations', verbose_name='Товар')

    sku = models.CharField('Артикул', max_length=50, unique=True,
                           validators = [RegexValidator(regex='^[A-Z0-9-]+$',
                                         message='Артикул может содержать только заглавные буквы,цифры и дефис')])

    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators = [MinValueValidator(0)])
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания',auto_now_add=True)

    class Meta:
        verbose_name = 'Вариация'
        verbose_name_plural = 'Вариации'
        indexes = [
            models.Index(fields = ['product']),
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

class Stock(models.Model):
    """Остатки товаров на складах"""
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='stocks', verbose_name='Вариация')
    warehouse_id = models.IntegerField('ID склада', default=1, validators = [MinValueValidator(1)])
    quantity = models.IntegerField('Количество', default=0, validators = [MinValueValidator(0)])
    reserved = models.IntegerField('Зарезервировано', default=0, validators = [MinValueValidator(0)])

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
        unique_together = ('variation', 'warehouse_id')
        indexes = [
            models.Index(fields=['variation']),
            models.Index(fields=['warehouse_id']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(reserved__lte=models.F('quantity')),
                name='reserved_lte_quantity'
            )
        ]
    def __str__(self):
        return f"{self.variation.sku} - склад {self.warehouse_id}: {self.quantity} шт"

    @property
    def available(self):
        """Доступное количество (без резерва)"""
        return self.quantity - self.reserved
