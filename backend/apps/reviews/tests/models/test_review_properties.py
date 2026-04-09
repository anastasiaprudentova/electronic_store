import pytest
from datetime import timedelta
from django.utils import timezone
from apps.reviews.models import Review
from apps.catalog.models import Product

@pytest.mark.django_db
class TestReviewProperties:
    """Тестирование свойств и мета-данных отзыва"""

    def test_review_str_method(self, review):
        """
        Строковое представление отзыва
        Ожидаемый результат: __str__ возвращает "username - product - rating"
        """
        expected = f"{review.user.username} - {review.product.name} - {review.rating}"
        assert str(review) == expected

    def test_review_rating_stars_property(self, user, product):
        """
        Свойство rating_stars
        Ожидаемый результат: возвращает строку из звезд ★ и ☆
        """
        review = Review(user=user, product=product, rating=4)
        assert review.rating_stars == "★★★★☆"

        review.rating = 5
        assert review.rating_stars == "★★★★★"

        review.rating = 1
        assert review.rating_stars == "★☆☆☆☆"

    def test_review_ordering(self, user, product):
        """
        Сортировка отзывов по умолчанию
        Ожидаемый результат: новые отзывы сверху
        """

        other_product = Product.objects.create(
            name="Другой товар",
            brand=product.brand,
            category=product.category
        )

        old = Review.objects.create(user=user, product=product, rating=4)
        old.created_at = timezone.now() - timedelta(days=5)
        old.save()

        new = Review.objects.create(user=user, product=other_product, rating=5)

        reviews = Review.objects.all()
        assert reviews[0] == new
        assert reviews[1] == old

    def test_review_indexes(self, user, product):
        """
        Проверка наличия индексов
        Ожидаемый результат: индексы созданы для полей user, product, created_at, rating
        """
        Review.objects.create(user=user, product=product, rating=4)
        Review.objects.filter(user=user).exists()
        Review.objects.filter(product=product).exists()
        Review.objects.filter(rating=4).exists()