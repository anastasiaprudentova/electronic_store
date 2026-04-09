import pytest
from django.contrib.auth.models import User
from apps.reviews.models import Review
from apps.catalog.models import Product


@pytest.mark.django_db
class TestReviewManager:
    """Тестирование ReviewManager"""

    def test_positive_returns_reviews_with_rating_4_or_5(self, user, product, review):
        """
        Фильтр положительных отзывов
        Ожидаемый результат: возвращает проверенные отзывы с рейтингом 4 или 5
        """
        positive = Review.objects.positive()
        assert review in positive

    def test_pending_returns_unmoderated_reviews(self, user, product):
        """
        Фильтр отзывов, ожидающих проверки
        Ожидаемый результат: возвращает только непроверенные отзывы
        """
        pending = Review.objects.create(user=user, product=product, rating=4, is_moderated=False)
        result = Review.objects.pending()
        assert pending in result

    def test_moderated_returns_approved_reviews(self, user, product, review):
        """
        Фильтр проверенных отзывов
        Ожидаемый результат: возвращает только проверенные отзывы
        """
        result = Review.objects.moderated()
        assert review in result

    def test_for_product_returns_reviews_for_specific_product(self, user, product, review):
        """
        Фильтр отзывов для конкретного товара
        Ожидаемый результат: возвращает отзывы только для указанного товара
        """
        product_reviews = Review.objects.for_product(product)
        assert review in product_reviews

    def test_with_rating_returns_reviews_with_specific_rating(self, user, product, review):
        """
        Фильтр отзывов с конкретной оценкой
        Ожидаемый результат: возвращает отзывы только с указанным рейтингом
        """
        rating_5 = Review.objects.with_rating(5)
        assert review in rating_5

    def test_last_review_returns_reviews_from_last_n_days(self, user, product, review):
        """
        Фильтр отзывов за последние N дней
        Ожидаемый результат: возвращает отзывы, созданные за указанный период
        """
        last_7 = Review.objects.last_review(days=7)
        assert review in last_7

    def test_average_rating_calculates_correctly(self, user, product):
        """
        Средний рейтинг товара
        Ожидаемый результат: возвращает среднее арифметическое всех проверенных отзывов
        """
        other_user = User.objects.create_user(username="other", password="123")
        third_user = User.objects.create_user(username="third", password="123")

        Review.objects.create(user=user, product=product, rating=5, is_moderated=True)
        Review.objects.create(user=other_user, product=product, rating=4, is_moderated=True)
        Review.objects.create(user=third_user, product=product, rating=3, is_moderated=False)

        avg = Review.objects.average_rating(product)
        assert avg == 4.5

    def test_average_rating_with_no_reviews(self, product):
        """
        Средний рейтинг при отсутствии отзывов
        Ожидаемый результат: возвращает 0
        """
        assert Review.objects.average_rating(product) == 0

    def test_rating_distribution_returns_correct_counts(self, user, product):
        """
        Распределение оценок
        Ожидаемый результат: возвращает словарь с количеством отзывов по каждой оценке
        """
        other_user = User.objects.create_user(username="other", password="123")
        other_product = Product.objects.create(
            name="Другой товар",
            brand=product.brand,
            category=product.category
        )

        Review.objects.create(user=user, product=product, rating=5, is_moderated=True)
        Review.objects.create(user=other_user, product=product, rating=5, is_moderated=True)
        Review.objects.create(user=user, product=other_product, rating=4, is_moderated=True)

        dist = Review.objects.rating_distribution()
        assert dist[5] == 2
        assert dist[4] == 1