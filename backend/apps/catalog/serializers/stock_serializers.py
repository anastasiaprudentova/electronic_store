from rest_framework import serializers
from ..models import Stock

class StockSerializer(serializers.ModelSerializer):
    """
    Сериализатор для остатков на складе
    """
    available = serializers.SerializerMethodField()
    variation_sku = serializers.CharField(source='variation.sku', read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'variation', 'variation_sku', 'warehouse_id',
            'quantity', 'reserved', 'available'
        ]

    def get_available(self, obj):
        """
        Вычисляет доступное количество (quantity - reserved)
        """
        return obj.available