from django.db import models

class TimeStampedModel(models.Model):
    """Абстрактная модель, добавляющая поля created_at и updated_at"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']