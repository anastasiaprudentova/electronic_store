from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админка для корзины пользователя"""
    list_display = ('user', 'product_info', 'quantity', 'item_total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'variation__product__name')
    readonly_fields = ('updated_at', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Товар', {
            'fields': ('variation', 'quantity')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_info(self,obj):
        """Информация о товаре"""
        return f"{obj.variation.product.name} ({obj.variation.sku})"
    product_info.short_description = 'Товар'

    def item_total(self, obj):
        """Стоимость позиции"""
        return f"{obj.total_price} ₽"
    item_total.short_description = 'Стоимость'