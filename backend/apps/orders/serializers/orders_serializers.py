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
    product_slug = serializers.CharField(source='variation.product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'variation', 'variation_info', 'product_name', 'product_slug', 'product_image',
            'quantity', 'price_per_unit', 'total_price'
        ]

    def get_product_image(self, obj):
        """
        Возвращает URL изображения товара для истории заказов
        """
        request = self.context.get('request')
        product = obj.variation.product

        main_gallery = product.gallery.filter(is_main=True).first()
        if main_gallery and main_gallery.image:
            url = main_gallery.image.url
            return request.build_absolute_uri(url) if request else url

        first_image = product.gallery.first()
        if first_image and first_image.image:
            url = first_image.image.url
            return request.build_absolute_uri(url) if request else url

        return None

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