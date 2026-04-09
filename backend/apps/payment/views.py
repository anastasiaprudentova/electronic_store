from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from apps.orders.models import Order, Payment
from .serializers import PaymentSerializer, CreatePaymentSerializer, UpdatePaymentStatusSerializer


class PaymentViewSet(viewsets.GenericViewSet):
    """API для платежей"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_order(self, order_id):
        """Получить заказ с проверкой прав"""
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

        if not self.request.user.is_staff and order.user != self.request.user:
            return None
        return order

    def retrieve(self, request, order_id=None):
        """Просмотр платежа"""
        order = self.get_order(order_id)
        if not order:
            return Response({'success': False, 'message': 'Заказ не найден'}, status=404)

        payment = Payment.objects.filter(order=order).first()
        if not payment:
            return Response({'success': False, 'message': 'Платёж не создан'}, status=404)

        return Response(PaymentSerializer(payment, context={'request': request}).data)

    def create(self, request, order_id=None):
        """Создание платежа"""
        order = self.get_order(order_id)
        if not order:
            return Response({'success': False, 'message': 'Заказ не найден'}, status=404)

        if Payment.objects.filter(order=order).exists():
            return Response({'success': False, 'message': 'Платёж уже существует'}, status=400)

        if order.status in ['cancelled', 'delivered', 'paid']:
            return Response({'success': False, 'message': 'Нельзя оплатить этот заказ'}, status=400)

        serializer = CreatePaymentSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)

        payment = Payment.objects.create(
            order=order,
            method=serializer.validated_data['method'],
            amount=order.total_amount
        )

        return Response({
            'success': True,
            'message': 'Платёж создан',
            'payment': PaymentSerializer(payment, context={'request': request}).data
        }, status=201)

    def partial_update(self, request, order_id=None):
        """Обновление статуса платежа (админ)"""
        if not request.user.is_staff:
            return Response({'success': False, 'message': 'Доступ запрещён'}, status=403)

        order = self.get_order(order_id)
        if not order:
            return Response({'success': False, 'message': 'Заказ не найден'}, status=404)

        payment = Payment.objects.filter(order=order).first()
        if not payment:
            return Response({'success': False, 'message': 'Платёж не найден'}, status=404)

        serializer = UpdatePaymentStatusSerializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if payment.status == 'completed':
            order.status = 'paid'
            order.save()

        return Response({
            'success': True,
            'message': 'Статус обновлён',
            'payment': PaymentSerializer(payment, context={'request': request}).data
        })