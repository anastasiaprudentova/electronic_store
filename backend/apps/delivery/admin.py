from django.contrib import admin
from .models import Delivery

class DeliveryInline(admin.TabularInline):
    """Отображает доставку заказа."""
    model = Delivery
    extra = 1
    fields = ('delivery_type', 'address', 'pickup_point', 'tracking_number', 'status')
    can_delete = False

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    """Отображает доставку"""
    list_display = ('order', 'delivery_type', 'status', 'tracking_number', 'carrier')
    list_filter = ('delivery_type', 'status', 'carrier')
    search_fields = ('order__order_number', 'tracking_number')