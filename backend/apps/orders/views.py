import logging

from apps.cart.models import Cart
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Order, OrderItem
from .serializers import (
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    UpdateOrderStatusSerializer,
)

logger = logging.getLogger(__name__)


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
        logger.info(f"Пользователь {request.user.email} запросил список заказов")
        orders = self.get_queryset()
        logger.debug(f"Найдено {orders.count()} заказов")
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Детали заказа"""
        logger.info(f"Пользователь {request.user.email} запросил детали заказа {pk}")
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            logger.warning(f"Заказ {pk} не найден")
            return Response(
                {"success": False, "message": "Заказ не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def create(self, request):
        """Создание заказа"""

        logger.info(f"Пользователь {request.user.email} создаёт заказ")
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            logger.warning(
                f"Пользователь {request.user.email} пытается создать пустой заказ"
            )
            return Response(
                {"success": False, "message": "Корзина пуста"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CreateOrderSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        total_amount = Cart.objects.total_price_for_user(request.user)
        logger.debug(f"Общая сумма заказа: {total_amount}")

        try:
            order = Order.objects.create(
                user=request.user,
                address=serializer.validated_data["address"],
                comment=serializer.validated_data.get("comment", ""),
                total_amount=total_amount,
            )
            logger.info(f"Создан заказ #{order.id} на сумму {order.total_amount}")

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variation=item.variation,
                    quantity=item.quantity,
                    price_per_unit=item.variation.price,
                    total_price=item.variation.price * item.quantity,
                )
                logger.debug(f"Товар {item.variation.id} перенесён в заказ #{order.id}")

            Cart.objects.clear_cart(request.user)
            logger.info(f"Корзина пользователя {request.user.email} очищена")

            return Response(
                {
                    "success": True,
                    "message": "Заказ успешно создан",
                    "order": OrderDetailSerializer(order).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"Ошибка при создании заказа: {str(e)}", exc_info=True)
            return Response(
                {"success": False, "message": "Ошибка при создании заказа"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def status(self, request, pk=None):
        """Обновление статуса заказа (только для админов)"""
        logger.info(f"Админ {request.user.email} обновляет статус заказа {pk}")

        try:
            order = self.get_queryset().get(pk=pk)
            old_status = order.get_status_display()
        except Order.DoesNotExist:
            logger.warning(f"Заказ {pk} не найден при попытке обновить статус")
            return Response(
                {"success": False, "message": "Заказ не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdateOrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(
            f"Статус заказа #{order.id} изменён с '{old_status}' на '{order.get_status_display()}'"
        )

        return Response(
            {
                "success": True,
                "message": f"Статус заказа изменён на {order.get_status_display()}",
            }
        )
