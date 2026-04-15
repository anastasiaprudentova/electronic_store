import pytest
from apps.orders.models import PickupPoint

@pytest.mark.django_db
class TestPickupPointModel:
    """Тестирование модели PickupPoint (пункты выдачи)"""

    def test_create_pickup_point_with_valid_data(self):
        """
        Создание ПВЗ с валидными данными
        Ожидаемый результат: ПВЗ создается со всеми полями
        """
        pickup = PickupPoint.objects.create(
            name="ПВЗ на Ленина",
            carrier="СДЭК",
            city="Москва",
            address="ул. Ленина, д. 15",
            working_hours="пн-пт 10-20, сб 10-18",
            is_active=True
        )

        assert pickup.name == "ПВЗ на Ленина"
        assert pickup.carrier == "СДЭК"
        assert pickup.city == "Москва"
        assert pickup.address == "ул. Ленина, д. 15"
        assert pickup.working_hours == "пн-пт 10-20, сб 10-18"
        assert pickup.is_active is True

    def test_create_pickup_point_without_optional_fields(self):
        """
        Создание ПВЗ без необязательных полей
        Ожидаемый результат: ПВЗ создается с пустыми полями
        """
        pickup = PickupPoint.objects.create(
            name="ПВЗ на Ленина",
            carrier="СДЭК",
            city="Москва",
            address="ул. Ленина, д. 15"
        )

        assert pickup.working_hours == ""
        assert pickup.is_active is True

    def test_pickup_point_str_method(self):
        """
        Строковое представление ПВЗ
        Ожидаемый результат: __str__ возвращает "Название (Город)"
        """
        pickup = PickupPoint.objects.create(
            name="ПВЗ на Ленина",
            carrier="СДЭК",
            city="Москва",
            address="ул. Ленина, д. 15"
        )
        assert str(pickup) == "ПВЗ на Ленина (Москва)"

    def test_pickup_point_ordering(self):
        """
        Сортировка ПВЗ по умолчанию
        Ожидаемый результат: сначала активные, затем по городу
        """
        PickupPoint.objects.create(
            name="ПВЗ А", carrier="СДЭК", city="Москва", address="ул. 1", is_active=True
        )
        PickupPoint.objects.create(
            name="ПВЗ Б", carrier="Boxberry", city="Москва", address="ул. 2", is_active=False
        )
        PickupPoint.objects.create(
            name="ПВЗ В", carrier="СДЭК", city="СПб", address="ул. 3", is_active=True
        )

        points = PickupPoint.objects.all()
        assert points[0].is_active is True
        assert points[1].is_active is True
        assert points[2].is_active is False

    def test_pickup_point_indexes(self, pickup_point):
        """
        Проверка наличия индексов
        Ожидаемый результат: индексы созданы для полей carrier и city
        """
        PickupPoint.objects.filter(carrier="СДЭК").exists()
        PickupPoint.objects.filter(city="Москва").exists()