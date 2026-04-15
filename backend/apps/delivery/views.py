from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import Delivery, PickupPoint
from .serializers import (DeliverySerializer, CreateDeliverySerializer, UpdateDeliverySerializer, PickupPointSerializer)
from apps.orders.models import Order


class PickupPointViewSet(viewsets.ReadOnlyModelViewSet):
    """API для пунктов выдачи (ПВЗ)"""
    queryset = PickupPoint.objects.filter(is_active=True)
    serializer_class = PickupPointSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    search_fields = ['name', 'city', 'carrier']
    filterset_fields = ['carrier', 'city', 'is_active']


class DeliveryViewSet(viewsets.GenericViewSet):
    """API для доставки заказа"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        """Доставки, доступные пользователю"""
        if self.request.user.is_staff:
            return Delivery.objects.all()
        return Delivery.objects.filter(order__user=self.request.user)

    def get_order(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

        if not self.request.user.is_staff and order.user != self.request.user:
            return None
        return order

    def retrieve(self, request, order_id=None):
        """Просмотр доставки для заказа"""
        order = self.get_order(order_id)
        if not order:
            return Response({
                'success': False,
                'message': 'Заказ не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            delivery = Delivery.objects.get(order=order)
            serializer = DeliverySerializer(delivery, context={'request': request})
            return Response(serializer.data)
        except Delivery.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Доставка для этого заказа ещё не создана'
            }, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, order_id=None):
        """Выбор способа доставки при оформлении заказа"""
        order = self.get_order(order_id)
        if not order:
            return Response({
                'success': False,
                'message': 'Заказ не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        if Delivery.objects.filter(order=order).exists():
            return Response({
                'success': False,
                'message': 'Доставка для этого заказа уже создана'
            }, status=status.HTTP_400_BAD_REQUEST)

        if order.status != 'new':
            return Response({
                'success': False,
                'message': f'Нельзя изменить доставку для заказа в статусе "{order.get_status_display()}"'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateDeliverySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        delivery = Delivery.objects.create(
            order=order,
            delivery_type=serializer.validated_data['delivery_type'],
            address_id=serializer.validated_data.get('address_id'),
            pickup_point_id=serializer.validated_data.get('pickup_point_id')
        )

        return Response({
            'success': True,
            'message': 'Способ доставки выбран',
            'delivery': DeliverySerializer(delivery, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, order_id=None):
        """Обновление статуса доставки (только для админов)"""
        if not request.user.is_staff:
            return Response({
                'success': False,
                'message': 'Только администраторы могут обновлять статус доставки'
            }, status=status.HTTP_403_FORBIDDEN)

        order = self.get_order(order_id)
        if not order:
            return Response({
                'success': False,
                'message': 'Заказ не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            delivery = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Доставка для этого заказа не найдена'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateDeliverySerializer(delivery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'message': 'Статус доставки обновлён',
            'delivery': DeliverySerializer(delivery, context={'request': request}).data
        })