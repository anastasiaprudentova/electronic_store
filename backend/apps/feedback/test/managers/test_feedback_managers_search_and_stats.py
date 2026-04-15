import pytest
from apps.feedback.models import Feedback

@pytest.mark.django_db
class TestFeedbackManagerSearchAndStats:
    """Тестирование методов поиска и статистики менеджера Feedback"""
    def test_search_manager(self, feedback_new, all_feedbacks):
        """
        Проверка поиска обращений по теме и сообщению
        Ожидаемый результат: возвращаются обращения, содержащие поисковый запрос
        """

        result = Feedback.objects.search('Новое обращение')
        assert result.count() == 1
        assert feedback_new in result
        result = Feedback.objects.search('Текст сообщения')
        assert result.count() == 5
        result = Feedback.objects.search('несуществующее слово')
        assert result.count() == 0
        result = Feedback.objects.search('')
        assert result.count() == 0

    def test_statistics_manager(self, all_feedbacks):
        """
        Проверка получения статистики по обращениям
        Ожидаемый результат: словарь с корректными счетчиками
        """
        stats = Feedback.objects.statistics()

        assert stats['total'] == 5
        assert stats['new'] == 2
        assert stats['in_progress'] == 1
        assert stats['responded'] == 1
        assert stats['closed'] == 1
        assert stats['without_response'] == 3
        assert stats['with_response'] == 2