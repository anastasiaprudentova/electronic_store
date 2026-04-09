from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, CreateOrderSerializer,
    UpdateOrderStatusSerializer, PaymentSerializer)
from apps.cart.models import Cart


class OrderViewSet(viewsets.GenericViewSet):
    """API для заказов"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def list(self, request):
        """Список заказов пользователя"""
        orders = self.get_queryset()
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Детали заказа"""
        order = self.get_queryset().get(pk=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create(self, request):
        """Создание заказа"""
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(
            user=request.user,
            address=serializer.validated_data['address'],
            comment=serializer.validated_data.get('comment', ''),
            total_amount=Cart.objects.total_price_for_user(request.user)
        )

        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variation=item.variation,
                quantity=item.quantity,
                price_per_unit=item.variation.price,
                total_price=item.variation.price * item.quantity
            )
        Cart.objects.clear_cart(request.user)

        return Response({
            'success': True,
            'message': 'Заказ успешно создан',
            'order': OrderDetailSerializer(order).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def status(self, request, pk=None):
        """Обновление статуса заказа (только для админов)"""
        order = self.get_queryset().get(pk=pk)
        serializer = UpdateOrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'message': f'Статус заказа изменён на {order.get_status_display()}'
        })