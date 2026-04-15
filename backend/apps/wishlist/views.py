from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Wishlist
from .serializers import WishlistSerializer, AddToWishlistSerializer


@method_decorator(cache_page(60 * 5), name='dispatch')
class WishlistViewSet(viewsets.GenericViewSet):
    """API для избранного"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def list(self, request):
        """Список избранного"""
        wishlist = self.get_queryset()
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Добавление в избранное"""
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product_id=serializer.validated_data['product_id']
        )

        return Response({
            'success': True,
            'message': 'Товар добавлен в избранное' if created else 'Товар уже в избранном'
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Удаление из избранного"""
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        deleted, _ = Wishlist.objects.filter(
            user=request.user,
            product_id=serializer.validated_data['product_id']
        ).delete()

        return Response({
            'success': deleted,
            'message': 'Товар удалён из избранного' if deleted else 'Товар не найден'
        })