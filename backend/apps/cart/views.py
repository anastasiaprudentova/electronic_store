import logging

from apps.catalog.models import Variation
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Cart
from .serializers import CartSerializer, UpdateCartItemSerializer

logger = logging.getLogger(__name__)


class CartViewSet(viewsets.GenericViewSet):
    """API для корзины"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request):
        """Просмотр корзины"""
        logger.info(f"Пользователь {request.user.email} запросил корзину")
        cart_items = self.get_queryset()
        total_price = Cart.objects.total_price_for_user(request.user)
        total_quantity = Cart.objects.items_count(request.user)
        logger.debug(f"В корзине {cart_items.count()} позиций на сумму {total_price}")

        data = {
            "items": cart_items,
            "total_price": total_price,
            "total_quantity": total_quantity,
            "items_count": cart_items.count(),
        }
        serializer = CartSerializer(data, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        """Добавление товара в корзину"""
        variation_id = request.data.get("variation_id")
        quantity = request.data.get("quantity", 1)

        logger.info(
            f"Пользователь {request.user.email} добавляет товар {variation_id}, кол-во: {quantity}"
        )

        # Проверка variation_id
        if not variation_id:
            logger.warning(f"Пользователь {request.user.email} не указал variation_id")
            return Response(
                {
                    "success": False,
                    "message": "Не указан ID товара",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Проверяем наличия вариации
            variation = Variation.objects.filter(
                id=variation_id, is_active=True
            ).first()
            if not variation:
                logger.warning(
                    f"Попытка добавить несуществующий или неактивный товар {variation_id}"
                )
                return Response(
                    {
                        "success": False,
                        "message": "Товар не найден или недоступен",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            cart_item, created = Cart.objects.add_item(
                user=request.user,
                variation_id=variation_id,
                quantity=quantity,
            )

            if created:
                logger.info(
                    f"Товар {variation_id} ({variation.product.name}) добавлен в корзину пользователя {request.user.email}"
                )
            else:
                logger.info(
                    f"Количество товара {variation_id} увеличено до {cart_item.quantity}"
                )

            return Response(
                {
                    "success": True,
                    "message": "Товар добавлен в корзину",
                    "item": CartSerializer(
                        cart_item, context={"request": request}
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"Ошибка при добавлении в корзину: {str(e)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "message": "Внутренняя ошибка сервера",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def remove(self, request):
        """Удаление товара из корзины"""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = Cart.objects.remove_item(
            request.user, serializer.validated_data["variation_id"]
        )

        if success:
            logger.info(
                f"Пользователь {request.user.email} удалил товар {serializer.validated_data['variation_id']} из корзины"
            )
        else:
            logger.warning(
                f"Попытка удалить несуществующий товар {serializer.validated_data['variation_id']} из корзины"
            )

        return Response(
            {
                "success": success,
                "message": "Товар удалён из корзины" if success else "Товар не найден",
            }
        )

    @action(detail=False, methods=["post"])
    def update(self, request):
        """Обновление количества товара"""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = Cart.objects.update_quantity(
            request.user,
            serializer.validated_data["variation_id"],
            serializer.validated_data["quantity"],
        )

        if success:
            logger.info(
                f"Пользователь {request.user.email} обновил количество товара {serializer.validated_data['variation_id']} до {serializer.validated_data['quantity']}"
            )
        else:
            logger.warning(
                f"Попытка обновить количество несуществующего товара {serializer.validated_data['variation_id']}"
            )

        return Response(
            {
                "success": success,
                "message": "Количество обновлено" if success else "Товар не найден",
            }
        )

    @action(detail=False, methods=["post"])
    def clear(self, request):
        """Очистка корзины"""
        cart_items_count = self.get_queryset().count()
        Cart.objects.clear_cart(request.user)
        logger.info(
            f"Пользователь {request.user.email} очистил корзину (удалено {cart_items_count} позиций)"
        )
        return Response({"success": True, "message": "Корзина очищена"})
