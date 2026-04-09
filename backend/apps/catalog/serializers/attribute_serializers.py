from rest_framework import serializers
from ..models import Attribute, AttributeValue

class AttributeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для характеристики
    """
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'type', 'unit']

class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Сериализатор для значения характеристики (READ)
    """
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    attribute_type = serializers.CharField(source='attribute.type', read_only=True)
    attribute_unit = serializers.CharField(source='attribute.unit', read_only=True)

    class Meta:
        model = AttributeValue
        fields = [
            'id', 'attribute', 'attribute_name', 'attribute_type', 'attribute_unit',
            'text_value', 'number_value', 'boolean_value'
        ]