import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from apps.feedback.models import Feedback

@pytest.fixture
def user(db):
    """Обычный пользователь"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Тест',
        last_name='Пользователь'
    )

@pytest.fixture
def user1(db):
    """Пользователь 1"""
    return User.objects.create_user(
        username='user1', email='user1@test.com', password='test'
    )

@pytest.fixture
def user2(db):
    """Пользователь 2"""
    return User.objects.create_user(
        username='user2', email='user2@test.com', password='test'
    )

@pytest.fixture
def feedback_new(user1):
    """Новое обращение (статус 'new')"""
    return Feedback.objects.create(
        user=user1,
        category='order_quality',
        subject='Новое обращение',
        message='Текст сообщения',
        status='new'
    )

@pytest.fixture
def feedback_in_progress(user1):
    """Обращение в обработке (статус 'in_progress')"""
    return Feedback.objects.create(
        user=user1,
        category='delivery',
        subject='В обработке',
        message='Текст сообщения',
        status='in_progress'
    )

@pytest.fixture
def feedback_responded(user2):
    """Обращение с ответом (статус 'responded')"""
    return Feedback.objects.create(
        user=user2,
        category='staff_work',
        subject='С ответом',
        message='Текст сообщения',
        status='responded',
        admin_response='Ответ администратора'
    )

@pytest.fixture
def feedback_closed(user2):
    """Закрытое обращение (статус 'closed')"""
    return Feedback.objects.create(
        user=user2,
        category='other',
        subject='Закрытое',
        message='Текст сообщения',
        status='closed',
        admin_response='Закрыто'
    )

@pytest.fixture
def feedback_without_response(user1):
    """Обращение без ответа администратора"""
    return Feedback.objects.create(
        user=user1,
        category='payment',
        subject='Без ответа',
        message='Текст сообщения',
        status='new',
        admin_response=''
    )

@pytest.fixture
def all_feedbacks(feedback_new, feedback_in_progress, feedback_responded,
                   feedback_closed, feedback_without_response):
    """Все обращения"""
    return [feedback_new, feedback_in_progress, feedback_responded,
            feedback_closed, feedback_without_response]

@pytest.fixture
def old_feedback(user1):
    """Старое обращение (10 дней назад)"""
    old = Feedback.objects.create(
        user=user1,
        category='other',
        subject='Старое',
        message='Старое сообщение'
    )
    old.created_at = timezone.now() - timedelta(days=10)
    old.save()
    return old

@pytest.fixture
def yesterday_feedback(user1):
    """Вчерашнее обращение"""
    yesterday = Feedback.objects.create(
        user=user1,
        category='other',
        subject='Вчерашнее',
        message='Сообщение'
    )
    yesterday.created_at = timezone.now() - timedelta(days=1)
    yesterday.save()
    return yesterday