from rest_framework import serializers
from ..models import Address

class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для адреса
    """
    class Meta:
        model = Address
        fields = [
            'id', 'recipient_name', 'phone', 'city', 'street', 'house',
            'apartment', 'postal_code', 'is_default'
        ]

    def validate(self, data):
        """
        Если адрес становится основным, снимает флаг с других адресов.
        """
        if data.get('is_default') and self.instance is None:
            user = self.context['request'].user
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return data


class AddressListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка адресов
    """

    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'house', 'apartment', 'is_default']

class CreateAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания адреса
    """

    class Meta:
        model = Address
        fields = ['recipient_name', 'phone', 'city', 'street', 'house', 'apartment', 'postal_code', 'is_default']

    def validate(self, data):
        """
        Если создается основной адрес, снимает флаг с других.
        """
        if data.get('is_default'):
            user = self.context['request'].user
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return data