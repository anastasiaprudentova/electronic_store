from apps.catalog.models import Variation
from rest_framework import serializers

from ..models import Cart


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для одной позиции в корзине
    """

    variation_id = serializers.IntegerField(source="variation.id", read_only=True)
    product_name = serializers.CharField(
        source="variation.product.name", read_only=True
    )
    product_slug = serializers.CharField(
        source="variation.product.slug", read_only=True
    )
    product_image = serializers.SerializerMethodField()
    price = serializers.DecimalField(
        source="variation.price", max_digits=10, decimal_places=2, read_only=True
    )
    sku = serializers.CharField(source="variation.sku", read_only=True)

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "variation_id",
            "product_name",
            "product_slug",
            "product_image",
            "sku",
            "price",
            "quantity",
            "total",
        ]

    def get_total(self, obj):
        return obj.quantity * obj.variation.price

    def get_product_image(self, obj):
        """
        Возвращает URL изображения товара для корзины
        """
        request = self.context.get("request")
        product = obj.variation.product

        # Ищем главное изображение в галерее
        main_gallery = product.gallery.filter(is_main=True).first()
        if main_gallery and main_gallery.image:
            url = main_gallery.image.url
            return request.build_absolute_uri(url) if request else url

        # Первое изображение в галерее
        first_image = product.gallery.first()
        if first_image and first_image.image:
            url = first_image.image.url
            return request.build_absolute_uri(url) if request else url

        return None


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

    variation_id = serializers.IntegerField(
        required=True, help_text="ID вариации товара"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        default=1,
        required=False,
        help_text="Количество товара (минимум 1)",
    )

    def validate_variation_id(self, value):
        if not Variation.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Товар не найден или недоступен")
        return value


class UpdateCartItemRequestSerializer(serializers.Serializer):
    """
    Входящие данные для обновления количества товара.
    """

    quantity = serializers.IntegerField(
        min_value=1, required=True, help_text="Новое количество товара"
    )


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
