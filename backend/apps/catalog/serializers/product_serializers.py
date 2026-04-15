from apps.reviews.models import Review
from rest_framework import serializers

from ..models import Product, ProductImage
from .attribute_serializers import AttributeValueSerializer
from .brand_serializers import BrandSerializer
from .category_serializers import CategorySerializer
from .variation_serializers import VariationSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений галереи
    """

    url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "url", "thumbnail_url", "alt_text", "order", "is_main"]

    def get_url(self, obj):
        """Полный URL изображения"""
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None

    def get_thumbnail_url(self, obj):
        """URL миниатюры"""
        return self.get_url(obj)


class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка товаров
    """

    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    main_price = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "main_image",
            "main_price",
            "brand_name",
            "category_name",
        ]

    def get_main_price(self, obj):
        """
        Возвращает минимальную цену из всех вариаций
        """
        variation = obj.variations.filter(is_active=True).first()
        if variation:
            return variation.price
        return None

    def get_main_image(self, obj):
        request = self.context.get("request")
        return obj.get_main_image_url(request)


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной страницы товара
    """

    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    attributes = AttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )
    gallery = ProductImageSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "main_image",
            "gallery",
            "brand",
            "category",
            "variations",
            "attributes",
            "avg_rating",
            "reviews_count",
            "created_at",
            "updated_at",
        ]

    main_image = serializers.SerializerMethodField()

    def get_main_image(self, obj):
        request = self.context.get("request")
        return obj.get_main_image_url(request)

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
