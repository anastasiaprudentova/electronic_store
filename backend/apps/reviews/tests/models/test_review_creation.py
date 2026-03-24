import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.reviews.models import Review

@pytest.mark.django_db
class TestReviewCreation:
    """Тестирование создания отзыва и валидации данных"""

    def test_create_review_with_valid_data(self, user, product):
        """
        Создание отзыва с валидными данными
        Ожидаемый результат: отзыв создается со всеми полями
        """
        review = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            comment="Отличный товар",
            advantages="Качество",
            disadvantages="Цена"
        )
        assert review.user == user
        assert review.product == product
        assert review.rating == 5
        assert review.comment == "Отличный товар"
        assert review.advantages == "Качество"
        assert review.disadvantages == "Цена"
        assert review.is_moderated is False

    def test_review_unique_user_product(self, user, product):
        """
        Уникальность пары пользователь-товар
        Ожидаемый результат: один пользователь может оставить только один отзыв на товар
        """
        Review.objects.create(user=user, product=product, rating=5)
        with pytest.raises(IntegrityError):
            Review.objects.create(user=user, product=product, rating=4)

    def test_review_rating_choices(self, user, product):
        """
        Проверка допустимых значений рейтинга
        Ожидаемый результат: рейтинг должен быть от 1 до 5
        """
        review = Review.objects.create(user=user, product=product, rating=3)
        assert review.rating == 3

        with pytest.raises(ValidationError):
            review = Review(user=user, product=product, rating=6)
            review.full_clean()

    def test_review_rating_validation(self, user, product):
        """
        Валидация рейтинга
        Ожидаемый результат: рейтинг не может быть меньше 1 или больше 5
        """
        with pytest.raises(ValidationError):
            review = Review(user=user, product=product, rating=0)
            review.full_clean()

        with pytest.raises(ValidationError):
            review = Review(user=user, product=product, rating=6)
            review.full_clean()

    def test_review_optional_fields(self, user, product):
        """
        Необязательные поля
        Ожидаемый результат: можно создать отзыв без комментария, достоинств и недостатков
        """
        review = Review.objects.create(user=user, product=product, rating=4)
        assert review.comment is None
        assert review.advantages == ""
        assert review.disadvantages == ""

    def test_review_is_moderated_default(self, user, product):
        """
        Значение is_moderated по умолчанию
        Ожидаемый результат: новый отзыв не проверен модератором
        """
        review = Review.objects.create(user=user, product=product, rating=4)
        assert review.is_moderated is False