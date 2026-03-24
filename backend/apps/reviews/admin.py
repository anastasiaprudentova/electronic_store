from django.contrib import admin
from django.utils.html import format_html
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов"""
    list_display = ('user', 'product', 'rating_stars_display', 'rating', 'is_moderated', 'created_at')
    list_filter = ('rating', 'is_moderated', 'created_at')
    search_fields = ('user__username', 'user__email', 'product__name', 'comment')
    list_editable = ('is_moderated',)
    readonly_fields = ('created_at', 'updated_at', 'rating_stars_display')
    ordering = ('-created_at',)

    fieldsets = (
        ('Пользователь и товар', {
            'fields': ('user', 'product')
        }),
        ('Оценка', {
            'fields': ('rating', 'rating_stars_display')
        }),
        ('Текст отзыва', {
            'fields': ('comment', 'advantages', 'disadvantages')
        }),
        ('Модерация', {
            'fields': ('is_moderated',),
            'classes': ('wide',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_stars_display(self, obj):
        """Отображение звезд рейтинга"""
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span>',
            obj.rating_stars
        )
    rating_stars_display.short_description = 'Рейтинг'

    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        """Одобрить выбранные отзывы"""
        updated = queryset.update(is_moderated=True)
        self.message_user(request, f"{updated} отзывов одобрено")

    approve_reviews.short_description = "Одобрить выбранные отзывы"

    def reject_reviews(self, request, queryset):
        """Отклонить выбранные отзывы"""
        updated = queryset.update(is_moderated=False)
        self.message_user(request, f"{updated} отзывов отклонено")

    reject_reviews.short_description = "Отклонить выбранные отзывы"