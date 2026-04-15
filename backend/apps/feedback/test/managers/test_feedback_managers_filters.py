import pytest
from apps.feedback.models import Feedback

@pytest.mark.django_db
class TestFeedbackManagerFilters:
    """Тестирование фильтрующих методов менеджера Feedback"""
    def test_new_manager(self, feedback_new, feedback_without_response,
                         feedback_in_progress, feedback_responded, feedback_closed):
        """
        Проверка получения новых обращений (статус 'new')
        Ожидаемый результат: возвращаются только обращения со статусом 'new'
        """
        result = Feedback.objects.new()
        assert result.count() == 2
        assert feedback_new in result
        assert feedback_without_response in result
        assert feedback_in_progress not in result
        assert feedback_responded not in result
        assert feedback_closed not in result

    def test_in_progress_manager(self, feedback_in_progress, feedback_new,
                                 feedback_responded, feedback_closed):
        """
        Проверка получения обращений в обработке (статус 'in_progress')
        Ожидаемый результат: возвращаются только обращения со статусом 'in_progress'
        """
        result = Feedback.objects.in_progress()
        assert result.count() == 1
        assert feedback_in_progress in result
        assert feedback_new not in result
        assert feedback_responded not in result
        assert feedback_closed not in result

    def test_responded_manager(self, feedback_responded, feedback_new,
                               feedback_in_progress, feedback_closed):
        """
        Проверка получения обращений с ответом (статус 'responded')
        Ожидаемый результат: возвращаются только обращения со статусом 'responded'
        """
        result = Feedback.objects.responded()
        assert result.count() == 1
        assert feedback_responded in result
        assert feedback_new not in result
        assert feedback_in_progress not in result
        assert feedback_closed not in result

    def test_closed_manager(self, feedback_closed, feedback_new,
                            feedback_in_progress, feedback_responded):
        """
        Проверка получения закрытых обращений (статус 'closed')
        Ожидаемый результат: возвращаются только обращения со статусом 'closed'
        """
        result = Feedback.objects.closed()
        assert result.count() == 1
        assert feedback_closed in result
        assert feedback_new not in result
        assert feedback_in_progress not in result
        assert feedback_responded not in result
    def test_by_user_manager(self, user1, user2, feedback_new, feedback_in_progress,
                             feedback_without_response, feedback_responded, feedback_closed):
        """
        Проверка получения обращений конкретного пользователя
        Ожидаемый результат: возвращаются только обращения указанного пользователя
        """
        result_user1 = Feedback.objects.by_user(user1)
        assert result_user1.count() == 3
        assert feedback_new in result_user1
        assert feedback_in_progress in result_user1
        assert feedback_without_response in result_user1
        assert feedback_responded not in result_user1
        assert feedback_closed not in result_user1

        result_user2 = Feedback.objects.by_user(user2)
        assert result_user2.count() == 2
        assert feedback_responded in result_user2
        assert feedback_closed in result_user2

    def test_by_category_manager(self, feedback_new, feedback_in_progress, feedback_closed):
        """
        Проверка получения обращений по категории
        Ожидаемый результат: возвращаются только обращения указанной категории
        """
        result = Feedback.objects.by_category('order_quality')
        assert result.count() == 1
        assert feedback_new in result

        result = Feedback.objects.by_category('delivery')
        assert result.count() == 1
        assert feedback_in_progress in result

        result = Feedback.objects.by_category('other')
        assert result.count() == 1
        assert feedback_closed in result

    def test_last_days_manager(self, all_feedbacks, old_feedback):
        """
        Проверка получения обращений за последние N дней
        Ожидаемый результат: возвращаются только обращения, созданные за последние N дней
        """
        result = Feedback.objects.last_days(7)
        assert result.count() == 5
        assert old_feedback not in result
        for feedback in all_feedbacks:
            assert feedback in result

    def test_today_manager(self, all_feedbacks, yesterday_feedback):
        """
        Проверка получения обращений, созданных сегодня
        Ожидаемый результат: возвращаются только обращения, созданные сегодня
        """
        result = Feedback.objects.today()
        assert result.count() == 5
        assert yesterday_feedback not in result
        for feedback in all_feedbacks:
            assert feedback in result

    def test_without_response_manager(self, feedback_new, feedback_in_progress,
                                      feedback_without_response, feedback_responded, feedback_closed):
        """
        Проверка получения обращений без ответа администратора
        Ожидаемый результат: возвращаются обращения с пустым admin_response
        """
        result = Feedback.objects.without_response()
        assert result.count() == 3
        assert feedback_new in result
        assert feedback_in_progress in result
        assert feedback_without_response in result
        assert feedback_responded not in result
        assert feedback_closed not in result