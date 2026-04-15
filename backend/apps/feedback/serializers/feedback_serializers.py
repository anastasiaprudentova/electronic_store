from rest_framework import serializers
from ..models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обратной связи
    """
    user_name = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_name', 'user_email',
            'category', 'category_display', 'subject', 'message',
            'status', 'status_display', 'admin_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'admin_response']

class CreateFeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания обращения (WRITE)
    Только для авторизованных пользователей
    """
    class Meta:
        model = Feedback
        fields = ['category', 'subject', 'message']

class AdminUpdateFeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления статуса и ответа (админ)
    """
    class Meta:
        model = Feedback
        fields = ['status', 'admin_response']