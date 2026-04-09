from rest_framework import serializers
from ..models import Order, OrderItem
from apps.catalog.serializers import VariationSerializer
from apps.users.serializers import AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для позиции заказа
    """
    product_name = serializers.CharField(source='variation.product.name', read_only=True)
    variation_info = VariationSerializer(source='variation', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'variation', 'variation_info', 'product_name',
            'quantity', 'price_per_unit', 'total_price'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка заказов
    """
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total_amount', 'status', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной страницы заказа
    """
    items = OrderItemSerializer(many=True, read_only=True)
    address_info = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'address', 'address_info',
            'total_amount', 'status', 'comment', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'order_number', 'user', 'created_at']


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания заказа
    """
    class Meta:
        model = Order
        fields = ['address', 'comment']

    def validate_address(self, value):
        """
        Проверяет, что адрес принадлежит текущему пользователю.
        """
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Этот адрес не принадлежит вам")
        return value


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления статуса заказа
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Проверяет корректность изменения статуса.
        """
        if self.instance and self.instance.status == 'delivered':
            raise serializers.ValidationError("Нельзя изменить статус доставленного заказа")
        return value