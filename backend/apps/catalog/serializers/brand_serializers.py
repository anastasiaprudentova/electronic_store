from rest_framework import serializers
from ..models import Brand

class BrandSerializer(serializers.ModelSerializer):
    """
    Сериализатор для бренда
    """
    class Meta:
        model = Brand
        fields = ['id', 'name']