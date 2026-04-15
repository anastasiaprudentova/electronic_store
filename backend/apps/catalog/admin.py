from django.contrib import admin
from django.utils.html import format_html

from .models import (Brand, Category, Product, ProductImage, AttributeValue, Attribute, Variation, Stock)

#Inline-классы
class AttributeValueInline(admin.TabularInline):
    """Отображает характеристики товара"""
    model = AttributeValue
    extra = 1
    fields = ('attribute', 'text_value', 'number_value', 'boolean_value')

class VariationInline(admin.TabularInline):
    """Отображает вариации товара"""
    model = Variation
    extra = 1
    fields = ('sku', 'price', 'is_active', 'created_at')
    readonly_fields = ('created_at',)

class StockInline(admin.TabularInline):
    """Отображает остатки на складах"""
    model = Stock
    extra = 1
    fields = ('warehouse_id', 'quantity', 'reserved', 'available')
    readonly_fields = ('available',)

class ProductImageInline(admin.TabularInline):
    """Галерея в карточке товара"""
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text', 'order', 'is_main', 'admin_thumbnail')
    readonly_fields = ('admin_thumbnail',)

    def admin_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет фото"
    admin_thumbnail.short_description = 'Превью'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админка для брендов"""
    list_display = ('name', 'product_count') #поля отображаемые в списке
    search_fields = ('name',) # поля поиска

    def product_count(self, obj):
        """Считает количество товаров этого бренда"""
        return obj.products.count()
    product_count.short_description = "Количество товаров"
    product_count.admin_order_field = 'product_count'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий"""
    list_display = ('name', 'parent', 'product_count')
    list_filter = ('parent',)
    search_fields = ('name',)

    def product_count(self, obj):
        """Считает количество товаров в категории"""
        return obj.products.count()
    product_count.short_description = 'Товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для товаров"""
    list_display = ('name', 'brand', 'category', 'variation_count', 'created_at')
    list_filter = ('brand', 'category', 'created_at',)
    search_fields = ('name', 'description',)
    list_editable = () # редактировать прямо в списке
    readonly_fields = ('created_at', 'updated_at') # поля, которые нельзя редактировать
    ordering = ('-created_at',)

    inlines = [ProductImageInline, AttributeValueInline, VariationInline]
    fieldsets = (('Основная информация', {'fields': ('name', 'description')}), ('Связи', {'fields': ('brand', 'category')}), ('Даты', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse')}))
    def variation_count(self, obj):
        """Показывает количество вариаций у товара"""
        count = obj.variations.count()
        if count > 0:
            url = f"/admin/catalog/variation/?product__id__exact={obj.id}"
            return format_html('<a href="{}">{} шт.</a>', url, count)
        return 0

    variation_count.short_description = 'Вариаций'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Отдельная админка для галереи"""
    list_display = ('id', 'product', 'admin_thumbnail', 'order', 'is_main')
    list_filter = ('product', 'is_main')
    list_editable = ('order', 'is_main')
    search_fields = ('product__name', 'alt_text')

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    """Админка для характеристик"""
    list_display = ('name', 'type', 'unit', 'values_count')
    list_filter = ('type',)
    search_fields = ('name',)

    def values_count(self, obj):
        """Показывает, сколько товаров имеют эту характеристику"""
        return obj.values.count()
    values_count.short_description = 'Использований'

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    """Админка для значений характеристик"""
    list_display = ('product', 'attribute', 'display_value')
    list_filter = ('attribute',)
    search_fields = ('product__name', 'attribute__name', 'text_value')

    def display_value(self, obj):
        """Показывает значение в зависимости от типа"""
        if obj.text_value:
            return obj.text_value
        if obj.number_value:
            return f"{obj.number_value} {obj.attribute.unit or ''}".strip()
        if obj.boolean_value is not None:
            return 'Да' if obj.boolean_value else 'Нет'
        return '-'

    display_value.short_description = 'Значение'

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """Админка для вариаций товаров"""
    list_display = ('sku','product','price','is_active','stock_info', 'created_at')
    list_filter = ('is_active', 'product__brand', 'product__category',)
    search_fields = ('sku', 'product__name',)
    list_editable = ('is_active', 'price')
    readonly_fields = ('created_at',)

    inlines = [StockInline]

    def stock_info(self,obj):
        """Информация об остатках"""
        stocks = obj.stocks.all()
        if stocks:
            total = sum(s.quantity for s in stocks)
            return f'{total} шт'
        return '-'
    stock_info.short_description = 'Остатки'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Админка для остатков на складах"""
    list_display = ('variation','warehouse_id','quantity','reserved','available','status')
    list_filter = ('warehouse_id',)
    search_fields = ('variation__sku', 'variation__product__name',)

    def available(self, obj):
        """Доступное количество"""
        return obj.available
    available.short_description = 'Доступно'

    def status(self, obj):
        """Статус наличия"""
        if obj.available > 0:
            return format_html('<span style="color: green;"> В наличии</span>')
        elif obj.quantity > 0:
            return format_html('<span style="color: orange;"> Зарезервировано</span>')
        else:
            return format_html('<span style="color: red;"> Нет</span>')
    status.short_description = 'Статус'