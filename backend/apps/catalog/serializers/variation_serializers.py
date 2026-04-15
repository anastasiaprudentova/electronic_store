from rest_framework import serializers
from ..models import Variation

class VariationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вариации товара (READ)
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Variation
        fields = ['id', 'product', 'product_name',
            'sku', 'price', 'old_price', 'is_active', 'created_at']