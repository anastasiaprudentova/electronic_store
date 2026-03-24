from rest_framework import serializers
from ..models import Cart
from apps.catalog.models import Variation

class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для одной позиции в корзине
    """
    variation_id = serializers.IntegerField(source='variation.id', read_only=True)
    product_name = serializers.CharField(source='variation.product.name', read_only=True)
    price = serializers.DecimalField(source='variation.price', max_digits=10, decimal_places=2, read_only=True)
    sku = serializers.CharField(source='variation.sku', read_only=True)

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'variation_id', 'product_name',
            'sku', 'price', 'quantity', 'total'
        ]

    def get_total(self, obj):
        return obj.quantity * obj.variation.price

class CartSummarySerializer(serializers.Serializer):
    """
    Краткая сводка по корзине
    """
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = serializers.IntegerField()
    items_count = serializers.IntegerField()

class AddToCartRequestSerializer(serializers.Serializer):
    """
    Входящие данные для добавления товара в корзину
    """
    variation_id = serializers.IntegerField(required=True, help_text="ID вариации товара")
    quantity = serializers.IntegerField(min_value=1, default=1, required=False, help_text="Количество товара (минимум 1)")

    def validate_variation_id(self, value):
        if not Variation.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Товар не найден или недоступен")
        return value

class UpdateCartItemRequestSerializer(serializers.Serializer):
    """
    Входящие данные для обновления количества товара.
    """
    quantity = serializers.IntegerField(min_value=1, required=True, help_text="Новое количество товара")

class AddToCartResponseSerializer(serializers.Serializer):
    """
    Исходящие данные после добавления товара.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    item = CartSerializer(read_only=True)
    cart_summary = CartSummarySerializer(read_only=True)

class CartResponseSerializer(serializers.Serializer):
    """
    Исходящие данные при просмотре корзины
    """
    items = CartSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = serializers.IntegerField()
    items_count = serializers.IntegerField()

class UpdateCartItemResponseSerializer(serializers.Serializer):
    """
    Исходящие данные после обновления количества.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    item = CartSerializer(read_only=True)
    cart_summary = CartSummarySerializer(read_only=True)

class DeleteCartItemResponseSerializer(serializers.Serializer):
    """
    Исходящие данные после удаления товара.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    cart_summary = CartSummarySerializer(read_only=True)

class ClearCartResponseSerializer(serializers.Serializer):
    """
    Исходящие данные после очистки корзины
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()