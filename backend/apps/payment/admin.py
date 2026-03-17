from django.contrib import admin
from .models import Payment

class PaymentInline(admin.StackedInline):
    """Отображает платеж по заказу."""
    model = Payment
    extra = 1
    fields = ('method', 'status', 'amount', 'paid_at')
    can_delete = False

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Отображает платежи"""
    list_display = ('order', 'method', 'status', 'amount', 'paid_at')
    list_filter = ('status', 'method')
    search_fields = ('order__order_number', 'transaction_id')