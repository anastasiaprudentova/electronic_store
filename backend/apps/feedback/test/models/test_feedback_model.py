import pytest
from apps.feedback.models import Feedback

@pytest.mark.django_db
class TestFeedbackModel:
    """Тестирование модели Feedback"""

    def test_create_feedback_by_authenticated_user(self, user):
        """
        Создание обращения авторизованным пользователем
        Ожидаемый результат: обращение создается, поле user заполнено, статус 'new'
        """
        feedback = Feedback.objects.create(
            user=user,
            category='order_quality',
            subject='Проблема с заказом',
            message='Заказ не пришел вовремя'
        )
        assert feedback.user == user
        assert feedback.category == 'order_quality'
        assert feedback.subject == 'Проблема с заказом'
        assert feedback.message == 'Заказ не пришел вовремя'
        assert feedback.status == 'new'

    def test_feedback_str_method(self, user):
        """
        Строковое представление объекта Feedback
        Ожидаемый результат: строка формата "username - subject (category_display)"
        """
        feedback = Feedback.objects.create(
            user=user,
            subject='Тестовая тема',
            category='other'
        )
        expected = f"{user.username} - Тестовая тема (Другое)"
        assert str(feedback) == expected

    def test_feedback_category_choices(self, user):
        """
        Проверка допустимых значений поля category
        Ожидаемый результат: все допустимые категории принимаются без ошибок
        """
        for category, _ in Feedback.CATEGORY_CHOICES:
            feedback = Feedback.objects.create(
                user=user,
                category=category,
                subject='Тест'
            )
            assert feedback.category == category

    def test_feedback_status_choices(self, user):
        """
        Проверка допустимых значений поля status
        Ожидаемый результат: все допустимые статусы принимаются без ошибок
        """
        for status, _ in Feedback.STATUS_CHOICES:
            feedback = Feedback.objects.create(
                user=user,
                status=status,
                subject='Тест'
            )
            assert feedback.status == status

    def test_feedback_ordering(self, user):
        """
        Проверка сортировки обращений по дате создания
        Ожидаемый результат: новые обращения идут первыми в списке
        """
        from datetime import timedelta
        from django.utils import timezone

        # Создаем старое обращение
        old = Feedback.objects.create(user=user, subject='Старое')
        old.created_at = timezone.now() - timedelta(days=5)
        old.save()

        # Создаем новое обращение
        new = Feedback.objects.create(user=user, subject='Новое')

        feedbacks = Feedback.objects.all()
        assert feedbacks[0] == new
        assert feedbacks[1] == old

    def test_feedback_default_status(self, user):
        """
        Проверка значения статуса по умолчанию
        Ожидаемый результат: статус автоматически устанавливается в 'new'
        """
        feedback = Feedback.objects.create(
            user=user,
            subject='Тест'
        )
        assert feedback.status == 'new'