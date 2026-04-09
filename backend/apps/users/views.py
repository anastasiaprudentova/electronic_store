from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User
from .serializers import (UserSerializer, RegisterSerializer, ChangePasswordSerializer)


class UserViewSet(viewsets.GenericViewSet):
    """API для пользователей"""
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация пользователя"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'success': True,
            'message': 'Регистрация успешно завершена',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Профиль пользователя"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'success': True,
                'message': 'Профиль обновлён',
                'user': serializer.data
            })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Смена пароля"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'success': False,
                'message': 'Неверный старый пароль'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'success': True,
            'message': 'Пароль успешно изменён'
        })