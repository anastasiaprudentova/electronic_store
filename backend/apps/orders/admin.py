from django.contrib import admin
from django.utils.html import format_html
from .models import PickupPoint, Order, OrderItem
from apps.payment.admin import PaymentInline
from apps.delivery.admin import DeliveryInline

#Inline-классы
class OrderItemInline(admin.TabularInline):
    """Отображает товары в заказе в виде таблицы"""
    model = OrderItem
    extra = 1
    fields = ('variation', 'quantity', 'price_per_unit', 'total_price')
    readonly_fields = ('price_per_unit', 'total_price')

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    """Отображает пункты выдачи в админке."""
    list_display = ('name', 'carrier', 'city', 'is_active', 'order_count')
    list_filter = ('is_active', 'carrier', 'city')
    search_fields = ('name', 'address')
    list_editable = ('is_active',)
    ordering = ('-is_active', 'city')

    def order_count(self, obj):
        """Показывает количество заказов, использующих этот ПВЗ."""
        count = obj.delivery_set.count()
        if count > 0:
            url = f"/admin/orders/delivery/?pickup_point__id__exact={obj.id}"
            return format_html('<a href="{}">{}</a>', url, count)
        return count
    order_count.short_description = 'Заказов'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображает заказы в админке"""
    list_display = ('order_number', 'user_info', 'total_amount', 'items_count', 'status_color', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__username')
    readonly_fields = ('order_number', 'created_at')
    ordering = ('-created_at',)

    inlines = [OrderItemInline, PaymentInline, DeliveryInline]

    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered']

    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'user', 'address', 'comment'),
            'description': 'Базовые данные о заказе'
        }),
        ('Финансы', {
            'fields': ('total_amount',),
            'classes': ('wide',),
        }),
        ('Статус', {
            'fields': ('status',),
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'Информация о времени создания'}),)

    def user_info(self, obj):
        """Возвращает email пользователя для отображения в списке"""
        return f"{obj.user.email}"
    user_info.short_description = 'Пользователь'

    def items_count(self, obj):
        """Подсчитывает количество товаров в заказе"""
        return obj.items.count()
    items_count.short_description = 'Товаров'

    def status_color(self, obj):
        """Отображает статус заказа разными цветами для наглядности"""
        colors = {
            'new': 'blue',
            'processing': 'orange',
            'paid': 'green',
            'shipped': 'purple',
            'delivered': 'darkgreen',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_color.short_description = 'Статус'

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = 'Отметить как оплаченные'

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Отметить как отправленные'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Отметить как доставленные'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Отображает позиции заказа"""
    list_display = ('order', 'variation', 'quantity', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('order__order_number', 'variation__sku')