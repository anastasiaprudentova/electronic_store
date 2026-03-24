from rest_framework import serializers
from ..models import Product
from apps.cart.models import Review
from .brand_serializers import BrandSerializer
from .category_serializers import CategorySerializer
from .variation_serializers import VariationSerializer
from .attribute_serializers import AttributeValueSerializer
class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка товаров
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        field = [
            'id', 'name', 'slug', 'main_image', 'main_price',
            'brand_name', 'category_name'
        ]

    def get_main_price(self, obj):
        """
        Возвращает минимальную цену из всех вариаций
        """
        variation = obj.variations.filter(is_active=True).first()
        if variation:
            return variation.price
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Возвращает минимальную цену из всех вариаций
    """
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    attributes = AttributeValueSerializer(source = "attribute_values", many = True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        field = [
            'id', 'name', 'slug', 'description', 'main_image',
            'brand', 'category', 'variations', 'attributes',
            'avg_rating', 'reviews_count', 'created_at', 'updated_at'
        ]

    def get_avg_rating(self, obj):
        """
        Возвращает средний рейтинг товара
        """
        return Review.objects.average_rating(obj)

    def get_reviews_count(self, obj):
        """
        Возвращает количество отзывов
        """
        return Review.objects.total_count(obj)