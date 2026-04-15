from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Address

#Inline-классы
class AddressInline(admin.TabularInline):
    """Отображает адреса"""
    model = Address
    extra = 0
    fields = ('recipient_name', 'city', 'street', 'house', 'apartment', 'postal_code', 'is_default')
    readonly_fields = ()


class CustomUserAdmin(UserAdmin):
    """Расширенная админка для пользователей с адресами"""
    inlines = [AddressInline]
    list_display = UserAdmin.list_display + ('username', 'email', 'get_addresses_count')

    def get_addresses_count(self, obj):
        """Количество адресов пользователя"""
        return obj.addresses.count()

    get_addresses_count.short_description = 'Адресов'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Админка для адресов доставки"""
    list_display = ('user', 'recipient_name', 'city', 'street', 'house', 'apartment', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('user__username', 'user__email', 'city', 'street', 'recipient_name')
    list_editable = ('is_default',)
    raw_id_fields = ('user',)
    ordering = ('user', '-is_default')

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Адресная информация', {
            'fields': ('recipient_name', 'city', 'street', 'house', 'apartment', 'postal_code')
        }),
        ('Настройки', {
            'fields': ('is_default',),
            'classes': ('wide',)
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)