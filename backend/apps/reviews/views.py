from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Review
from .serializers import (ReviewSerializer, CreateReviewSerializer, ModerateReviewSerializer)


@method_decorator(cache_page(60 * 10), name='dispatch')
class ReviewViewSet(viewsets.GenericViewSet):
    """API для отзывов"""
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return Review.objects.filter(product_id=product_id, is_moderated=True)
        return Review.objects.filter(is_moderated=True)

    def list(self, request):
        """Список отзывов (фильтр по товару)"""
        reviews = self.get_queryset()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create(self, request):
        """Создание отзыва"""
        serializer = CreateReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save(user=request.user)

        return Response({
            'success': True,
            'message': 'Отзыв успешно создан и отправлен на модерацию',
            'review': ReviewSerializer(review).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def moderate(self, request, pk=None):
        """Модерация отзыва (только для админов)"""
        review = Review.objects.get(pk=pk)
        serializer = ModerateReviewSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'message': 'Статус модерации обновлён'
        })