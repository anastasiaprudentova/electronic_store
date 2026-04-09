from rest_framework import serializers
from ..models import PickupPoint

class PickupPointSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пункта выдачи
    """
    class Meta:
        model = PickupPoint
        fields = [
            'id', 'name', 'carrier', 'city', 'address',
            'working_hours', 'is_active'
        ]