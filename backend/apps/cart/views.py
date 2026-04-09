from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Cart
from .serializers import (CartSerializer, AddToCartSerializer, UpdateCartItemSerializer)


class CartViewSet(viewsets.GenericViewSet):
    """API для корзины"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request):
        """Просмотр корзины"""
        cart_items = self.get_queryset()
        total_price = Cart.objects.total_price_for_user(request.user)
        total_quantity = Cart.objects.items_count(request.user)

        data = {
            'items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity,
            'items_count': cart_items.count()
        }
        serializer = CartSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Добавление товара в корзину"""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item, created = Cart.objects.add_item(
            user=request.user,
            variation_id=serializer.validated_data['variation_id'],
            quantity=serializer.validated_data.get('quantity', 1)
        )

        return Response({
            'success': True,
            'message': 'Товар добавлен в корзину',
            'item': CartSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Удаление товара из корзины"""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = Cart.objects.remove_item(
            request.user,
            serializer.validated_data['variation_id']
        )

        return Response({
            'success': success,
            'message': 'Товар удалён из корзины' if success else 'Товар не найден'
        })

    @action(detail=False, methods=['post'])
    def update(self, request):
        """Обновление количества товара"""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = Cart.objects.update_quantity(
            request.user,
            serializer.validated_data['variation_id'],
            serializer.validated_data['quantity']
        )

        return Response({
            'success': success,
            'message': 'Количество обновлено' if success else 'Товар не найден'
        })

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Очистка корзины"""
        Cart.objects.clear_cart(request.user)
        return Response({
            'success': True,
            'message': 'Корзина очищена'
        })