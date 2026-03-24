import pytest
from apps.catalog.models import Product
from apps.reviews.models import Review

@pytest.mark.django_db
class TestProductManager:
    def test_by_rating_returns_products_with_min_rating(self, product, user, review):
        """
        Ожидаемый результат: фильтр по рейтингу возвращает товары с рейтингом >= min_rating
        """
        results = Product.objects.rating(min_rating=4)
        assert product in results

    def test_by_rating_excludes_low_rated_products(self, product, user):
        """
        Ожидаемый результат: фильтр по рейтингу исключает товары с низким рейтингом.
        """
        Review.objects.create(
            user=user,
            product=product,
            rating=3,
            is_moderated=True
        )

        results = Product.objects.rating(min_rating=4)
        assert product not in results

    def test_by_rating_excludes_unmoderated_reviews(self, product, user):
        """
        Ожидаемый результат: при расчете рейтинга учитываются только проверенные отзывы
        """
        Review.objects.create(
            user=user,
            product=product,
            rating=5,
            is_moderated=False
        )

        results = Product.objects.rating(min_rating=4)
        assert product not in results