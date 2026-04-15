import pytest
from django.core.exceptions import ValidationError
from apps.users.models import Address

@pytest.mark.django_db
class TestAddressModel:
    """Тестирование модели Address (адреса доставки)"""

    def test_create_address_with_valid_data(self, user):
        """
        Создание адреса с валидными данными
        Ожидаемый результат: адрес создается со всеми полями
        """
        address = Address.objects.create(
            user=user,
            recipient_name="Иван Петров",
            phone="+7-999-123-45-67",
            city="Москва",
            street="Ленина",
            house="10",
            apartment="5",
            is_default=True
        )
        assert address.user == user
        assert address.city == "Москва"
        assert address.street == "Ленина"
        assert address.is_default is True

    def test_address_optional_fields(self, user):
        """
        Необязательные поля
        Ожидаемый результат: можно создать адрес с минимальным набором полей
        """
        address = Address.objects.create(user=user, city="Москва", street="Ленина")
        assert address.recipient_name == ""
        assert address.phone == ""
        assert address.house == ""

    def test_address_phone_validation(self, user):
        """
        Валидация номера телефона
        Ожидаемый результат: номер должен соответствовать формату
        """
        with pytest.raises(ValidationError):
            address = Address(user=user, city="Москва", street="Ленина", phone="abc")
            address.full_clean()

    def test_address_str_method(self, address):
        """
        Строковое представление адреса
        Ожидаемый результат: __str__ возвращает "Город, улица, д.дом, кв.квартира"
        """
        assert "Москва, Ленина" in str(address)

    def test_unique_default_address_per_user(self, user):
        """
        Уникальность основного адреса для пользователя
        Ожидаемый результат: у пользователя может быть только один адрес с is_default=True
        """
        Address.objects.create(user=user, city="Москва", street="Ленина", is_default=True)

        addr2 = Address.objects.create(user=user, city="СПб", street="Невский", is_default=True)

        addr1 = Address.objects.get(city="Москва")
        assert addr1.is_default is False
        assert addr2.is_default is True

    def test_multiple_non_default_addresses_allowed(self, user):
        """
        Несколько неосновных адресов
        Ожидаемый результат: у пользователя может быть много адресов с is_default=False
        """
        Address.objects.create(user=user, city="Москва", street="Ленина", is_default=True)
        Address.objects.create(user=user, city="СПб", street="Невский", is_default=False)
        assert Address.objects.filter(user=user).count() == 2
        assert Address.objects.filter(user=user, is_default=True).count() == 1

    def test_address_on_delete_cascade(self, user):
        """
        Каскадное удаление при удалении пользователя
        Ожидаемый результат: при удалении пользователя удаляются все его адреса
        """
        Address.objects.create(user=user, city="Москва", street="Ленина")
        user_id = user.id
        user.delete()
        assert Address.objects.filter(user_id=user_id).count() == 0

    def test_update_default_address(self, user):
        """
        Изменение основного адреса
        Ожидаемый результат: при установке нового основного адреса, старый становится неосновным
        """
        addr1 = Address.objects.create(user=user, city="Москва", street="Ленина", is_default=True)
        addr2 = Address.objects.create(user=user, city="СПб", street="Невский", is_default=False)
        addr2.is_default = True
        addr2.save()
        addr1.refresh_from_db()
        assert addr1.is_default is False
        assert addr2.is_default is True