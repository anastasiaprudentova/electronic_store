import logging

from apps.orders.models import Order, Payment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .serializers import (
    CreatePaymentSerializer,
    PaymentSerializer,
    UpdatePaymentStatusSerializer,
)

logger = logging.getLogger(__name__)


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
        logger.info(
            f"Пользователь {request.user.email} запросил платёж для заказа {order_id}"
        )
        order = self.get_order(order_id)

        if not order:
            logger.warning(f"Заказ {order_id} не найден при запросе платежа")
            return Response(
                {"success": False, "message": "Заказ не найден"}, status=404
            )

        payment = Payment.objects.filter(order=order).first()

        if not payment:
            logger.info(f"Платёж для заказа {order_id} ещё не создан")
            return Response(
                {"success": False, "message": "Платёж не создан"}, status=404
            )

        return Response(PaymentSerializer(payment, context={"request": request}).data)

    def create(self, request, order_id=None):
        """Создание платежа"""
        logger.info(
            f"Пользователь {request.user.email} создаёт платёж для заказа {order_id}"
        )

        order = self.get_order(order_id)
        if not order:
            logger.warning(f"Заказ {order_id} не найден при попытке оплаты")
            return Response(
                {"success": False, "message": "Заказ не найден"}, status=404
            )

        if Payment.objects.filter(order=order).exists():
            logger.warning(f"Попытка создать дублирующий платёж для заказа {order_id}")
            return Response(
                {"success": False, "message": "Платёж уже существует"}, status=400
            )

        if order.status in ["cancelled", "delivered", "paid"]:
            logger.warning(
                f"Попытка оплатить заказ {order_id} со статусом '{order.status}'"
            )
            return Response(
                {"success": False, "message": "Нельзя оплатить этот заказ"}, status=400
            )

        serializer = CreatePaymentSerializer(
            data=request.data, context={"order": order}
        )
        serializer.is_valid(raise_exception=True)

        try:
            payment = Payment.objects.create(
                order=order,
                method=serializer.validated_data["method"],
                amount=order.total_amount,
            )
            logger.info(
                f"Создан платёж #{payment.id} для заказа {order_id} на сумму {payment.amount}"
            )

            return Response(
                {
                    "success": True,
                    "message": "Платёж создан",
                    "payment": PaymentSerializer(
                        payment, context={"request": request}
                    ).data,
                },
                status=201,
            )

        except Exception as e:
            logger.error(
                f"Ошибка при создании платежа для заказа {order_id}: {str(e)}",
                exc_info=True,
            )
            return Response(
                {"success": False, "message": "Ошибка при создании платежа"},
                status=500,
            )

    def partial_update(self, request, order_id=None):
        """Обновление статуса платежа (админ)"""
        logger.info(
            f"Пользователь {request.user.email} обновляет статус платежа для заказа {order_id}"
        )

        if not request.user.is_staff:
            logger.warning(
                f"Неавторизованная попытка обновить статус платежа пользователем {request.user.email}"
            )
            return Response(
                {"success": False, "message": "Доступ запрещён"}, status=403
            )

        order = self.get_order(order_id)
        if not order:
            logger.warning(f"Заказ {order_id} не найден при обновлении статуса платежа")
            return Response(
                {"success": False, "message": "Заказ не найден"}, status=404
            )

        payment = Payment.objects.filter(order=order).first()
        if not payment:
            logger.warning(f"Платёж для заказа {order_id} не найден")
            return Response(
                {"success": False, "message": "Платёж не найден"}, status=404
            )

        old_status = payment.status
        serializer = UpdatePaymentStatusSerializer(
            payment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(
            f"Статус платежа #{payment.id} изменён с '{old_status}' на '{payment.status}'"
        )

        if payment.status == "completed":
            order.status = "paid"
            order.save()
            logger.info(f"Статус заказа #{order.id} обновлён на 'paid'")

        return Response(
            {
                "success": True,
                "message": "Статус обновлён",
                "payment": PaymentSerializer(
                    payment, context={"request": request}
                ).data,
            }
        )
