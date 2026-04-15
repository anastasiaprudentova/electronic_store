from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class FeedbackManager(models.Manager):
    """Менеджер для работы с обращениями обратной связи"""
    def new(self):
        """
        Новые обращения (статус 'new')
        """
        return self.filter(status='new')

    def in_progress(self):
        """
        Обращения в обработке (статус 'in_progress')
        """
        return self.filter(status='in_progress')

    def responded(self):
        """
        Обращения с ответом администратора (статус 'responded')
        """
        return self.filter(status='responded')

    def closed(self):
        """
        Закрытые обращения (статус 'closed')
        """
        return self.filter(status='closed')

    def by_user(self, user):
        """
        Обращения конкретного пользователя
        """
        return self.filter(user=user)

    def by_category(self, category):
        """
        Обращения по категории
        """
        return self.filter(category=category)

    def last_days(self, days=7):
        """
        Обращения за последние N дней
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff_date)

    def today(self):
        """
        Обращения, созданные сегодня
        """
        return self.filter(created_at__date=timezone.now().date())

    def search(self, query):
        """
        Поиск обращений по теме и сообщению
        """
        if not query:
            return self.none()
        return self.filter(Q(subject__icontains=query) | Q(message__icontains=query))

    def without_response(self):
        """
        Обращения без ответа администратора
        """
        return self.filter(
            Q(admin_response__isnull=True) | Q(admin_response__exact=''))

    def with_response(self):
        """
        Обращения с ответом администратора
        Ожидаемый результат: QuerySet обращений, у которых admin_response не пустой
        """
        return self.exclude(Q(admin_response__isnull=True) | Q(admin_response__exact=''))

    def statistics(self):
        """
        Статистика по обращениям
        """
        return {
            'total': self.count(),
            'new': self.new().count(),
            'in_progress': self.in_progress().count(),
            'responded': self.responded().count(),
            'closed': self.closed().count(),
            'without_response': self.without_response().count(),
            'with_response': self.with_response().count(),
        }