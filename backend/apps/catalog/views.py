from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Brand, Category, Product, Attribute, Variation, Stock
from .serializers import (
    BrandSerializer, CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    AttributeSerializer, VariationSerializer, StockSerializer)


# Кастомная пагинация для товаров
class ProductPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50


@method_decorator(cache_page(60 * 15), name='dispatch')
class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """API для брендов"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API для товаров"""
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'brand', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    pagination_class = ProductPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        """Для списка - краткий сериализатор, для деталей - полный"""
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer


@method_decorator(cache_page(60 * 30), name='dispatch')
class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """API для характеристик"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@method_decorator(cache_page(60 * 5), name='dispatch')
class VariationViewSet(viewsets.ReadOnlyModelViewSet):
    """API для вариаций товаров"""
    queryset = Variation.objects.filter(is_active=True)
    serializer_class = VariationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['product', 'is_active']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@method_decorator(cache_page(60 * 5), name='dispatch')
class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """API для остатков на складе"""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['variation', 'warehouse_id']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]