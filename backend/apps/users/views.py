import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializers import ChangePasswordSerializer, RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):
    """API для пользователей"""

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация пользователя"""
        email = request.data.get("email")
        username = request.data.get("username")

        logger.info(f"Попытка регистрации пользователя {username} ({email})")

        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            logger.info(
                f"Успешная регистрация пользователя {user.username} (ID: {user.id})"
            )

            return Response(
                {
                    "success": True,
                    "message": "Регистрация успешно завершена",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"Ошибка регистрации: {str(e)}")
            return Response(
                {
                    "success": False,
                    "message": "Ошибка регистрации. Проверьте введённые данные.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False, methods=["get", "patch"], permission_classes=[IsAuthenticated]
    )
    def profile(self, request):
        """Профиль пользователя"""
        logger.info(f"Пользователь {request.user.email} запросил профиль")

        if request.method == "GET":
            serializer = UserSerializer(request.user)
            logger.debug(f"Данные профиля: {serializer.data}")
            return Response(serializer.data)

        elif request.method == "PATCH":
            logger.info(f"Пользователь {request.user.email} обновляет профиль")
            try:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                logger.info(f"Профиль пользователя {request.user.email} обновлён")
                return Response(
                    {
                        "success": True,
                        "message": "Профиль обновлён",
                        "user": serializer.data,
                    }
                )
            except Exception as e:
                logger.error(f"Ошибка обновления профиля: {str(e)}")
                return Response(
                    {"success": False, "message": "Ошибка обновления профиля"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Смена пароля"""
        logger.info(f"Пользователь {request.user.email} пытается сменить пароль")

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            logger.warning(
                f"Неудачная попытка смены пароля для {user.email}: неверный старый пароль"
            )
            return Response(
                {"success": False, "message": "Неверный старый пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        logger.info(f"Пользователь {user.email} успешно сменил пароль")

        return Response({"success": True, "message": "Пароль успешно изменён"})
