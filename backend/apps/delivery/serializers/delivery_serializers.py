from rest_framework import serializers
from django.utils import timezone
from ..models import Delivery, PickupPoint
from apps.users.serializers import AddressSerializer
from apps.users.models import Address
from .pickup_point_serializers import PickupPointSerializer

class DeliverySerializer(serializers.ModelSerializer):
    """
    Сериализатор для доставки
    """
    address_info = AddressSerializer(source='address', read_only=True)
    pickup_point_info = PickupPointSerializer(source='pickup_point', read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'delivery_type', 'address', 'address_info', 'pickup_point',
            'pickup_point_info', 'tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'order']

class CreateDeliverySerializer(serializers.Serializer):
    """
    Сериализатор для выбора способа доставки
    """
    DELIVERY_TYPES = [
        ('courier', 'Курьер'),
        ('pickup', 'Пункт выдачи'),
    ]

    delivery_type = serializers.ChoiceField(choices=DELIVERY_TYPES, required=True, help_text="Тип доставки: courier или pickup")
    address_id = serializers.IntegerField(required=False, allow_null=True, help_text="ID адреса (для курьерской доставки)")
    pickup_point_id = serializers.IntegerField(required=False, allow_null=True, help_text="ID пункта выдачи (для доставки в ПВЗ)")

    def validate(self, data):
        """
        Проверяет корректность выбора способа доставки.
        """
        delivery_type = data.get('delivery_type')
        address_id = data.get('address_id')
        pickup_point_id = data.get('pickup_point_id')

        # Для курьерской доставки нужен адрес
        if delivery_type == 'courier' and not address_id:
            raise serializers.ValidationError({
                'address_id': 'Для курьерской доставки необходим адрес'
            })

        # Для доставки в ПВЗ нужен пункт выдачи
        if delivery_type == 'pickup' and not pickup_point_id:
            raise serializers.ValidationError({
                'pickup_point_id': 'Для доставки в ПВЗ необходим пункт выдачи'
            })

        # Нельзя указать и адрес, и ПВЗ одновременно
        if address_id and pickup_point_id:
            raise serializers.ValidationError(
                'Нельзя указать одновременно адрес и пункт выдачи'
            )

        return data

    def validate_address_id(self, value):
        """
        Проверяет, что адрес существует и принадлежит пользователю.
        """
        if value:
            user = self.context.get('request').user

            try:
                address = Address.objects.get(id=value)
            except Address.DoesNotExist:
                raise serializers.ValidationError("Адрес не найден")

            if address.user != user:
                raise serializers.ValidationError("Этот адрес не принадлежит вам")

        return value

    def validate_pickup_point_id(self, value):
        """
        Проверяет, что пункт выдачи существует и активен.
        """
        if value:
            try:
                pickup_point = PickupPoint.objects.get(id=value)
            except PickupPoint.DoesNotExist:
                raise serializers.ValidationError("Пункт выдачи не найден")

            if not pickup_point.is_active:
                raise serializers.ValidationError("Пункт выдачи временно недоступен")

        return value


class UpdateDeliverySerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления доставки
    """
    class Meta:
        model = Delivery
        fields = ['tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at']

    def validate(self, data):
        """
        Проверяет корректность изменения статуса.
        """
        status = data.get('status')
        shipped_at = data.get('shipped_at')
        delivered_at = data.get('delivered_at')

        # Автоматически устанавливаем дату отправки
        if status == 'shipped' and not shipped_at:
            data['shipped_at'] = timezone.now()

        # Автоматически устанавливаем дату доставки
        if status == 'delivered' and not delivered_at:
            data['delivered_at'] = timezone.now()

        # Дата доставки не может быть раньше даты отправки
        if shipped_at and delivered_at and delivered_at < shipped_at:
            raise serializers.ValidationError({
                'delivered_at': 'Дата доставки не может быть раньше даты отправки'
            })

        return data