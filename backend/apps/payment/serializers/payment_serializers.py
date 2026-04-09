from django.utils import timezone
from rest_framework import serializers
from ..models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежа
    """
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'method', 'status',
            'amount', 'paid_at', 'transaction_id'
        ]
        read_only_fields = ['id', 'order', 'transaction_id']

class CreatePaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания платежа
    """
    class Meta:
        model = Payment
        fields = ["method"]

    def validate(self, data):
        """
        Проверяет, что заказ существует и не оплачен.
        """
        order = self.context.get('order')
        if not order:
            raise serializers.ValidationError("Заказ не найден")
        if order.status == 'paid':
            raise serializers.ValidationError("Заказ уже оплачен")
        return data

class UpdatePaymentStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления статуса платежа
    """
    class Meta:
        model = Payment
        fields = ['status', 'transaction_id', 'paid_at']

    def validate(self, data):
        """
        Проверяет корректность изменения статуса.
        """
        status = data.get('status')
        transaction_id = data.get('transaction_id')

        if status == 'completed' and not transaction_id:
            raise serializers.ValidationError({
                'transaction_id': 'Для завершенного платежа необходим ID транзакции'
            })

        if status == 'completed':
            data['paid_at'] = timezone.now()

        return data