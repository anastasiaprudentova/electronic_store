from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзыва
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    rating_stars = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'user_email', 'product', 'product_name',
            'rating', 'rating_stars', 'comment', 'advantages', 'disadvantages', 'created_at','updated_at', 'is_moderated'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'is_moderated']

    def get_rating_stars(self, obj):
        return obj.rating_stars


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка отзывов
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    rating_stars = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user_name', 'rating',
            'rating_stars', 'comment', 'created_at'
        ]

    def get_rating_stars(self, obj):
        return obj.rating_stars

class CreateReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания отзыва
    """

    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment', 'advantages', 'disadvantages']

    def validate_rating(self, value):
        """Проверяет, что рейтинг от 1 до 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value

    def validate(self, data):
        """
        Проверяет, что пользователь еще не оставлял отзыв на этот товар.
        """
        user = self.context['request'].user
        product = data.get('product')

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на этот товар"
            )
        return data

class UpdateReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления отзыва
    """

    class Meta:
        model = Review
        fields = ['rating', 'comment', 'advantages', 'disadvantages']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value

class ModerateReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модерации отзыва
    """

    class Meta:
        model = Review
        fields = ['is_moderated']