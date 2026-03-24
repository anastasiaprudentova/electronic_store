from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Address(models.Model):
    """Адреса доставки пользователей"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Пользователь'
    )
    recipient_name = models.CharField('Получатель', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, validators=[
        RegexValidator(
            regex=r'^\+?[0-9\-\s()]+$',
            message='Введите корректный номер телефона'
        )
    ])
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=255)
    house = models.CharField('Дом', max_length=5, blank=True)
    apartment = models.CharField('Квартира', max_length=10, blank=True)
    postal_code = models.CharField('Индекс', max_length=10, blank=True)
    is_default = models.BooleanField('Основной адрес', default=False)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        indexes = [
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_default=True),
                name='unique_default_address_per_user'
            )
        ]

    def save(self, *args, **kwargs):
        """Автоматически сбрасывать is_default у других адресов"""
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.city, self.street]
        if self.house:
            parts.append(f"д.{self.house}")
        if self.apartment:
            parts.append(f"кв.{self.apartment}")
        return ", ".join(parts)