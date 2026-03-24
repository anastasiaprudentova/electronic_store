from rest_framework import serializers
from ..models import Wishlist
from apps.catalog.serializers import ProductListSerializer
from apps.catalog.models import Product

class WishlistSerializer(serializers.ModelSerializer):
    """
    Сериализатор для избранного
    """
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'id', 'product', 'product_id', 'product_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class WishlistListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'id', 'product_name', 'created_at'
        ]

class AddToWishlistSerializer(serializers.Serializer):
    """
    Сериализатор для добавления в избранное
    """
    product_id = serializers.IntegerField(required=True)

    def validate_product_id(self, value):
        """
        Проверяет, что товар существует и активен.
        """
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Товар не найден или недоступен")
        return value


class RemoveFromWishlistSerializer(serializers.Serializer):
    """
    Сериализатор для удаления из избранного
    """
    product_id = serializers.IntegerField(required=True)

    def validate_product_id(self, value):
        """
        Проверяет, что товар есть в избранном у пользователя.
        """
        user = self.context['request'].user
        if not Wishlist.objects.filter(user=user, product_id=value).exists():
            raise serializers.ValidationError("Товар не найден в избранном")
        return value