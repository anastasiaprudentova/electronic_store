import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.payment.models import Payment

@pytest.mark.django_db
class TestPaymentModel:
    """Тестирование модели Payment (платежи по заказам)"""

    def test_create_payment_with_valid_data(self, order):
        """
        Создание платежа с валидными данными
        Ожидаемый результат: платеж создается со всеми полями
        """
        payment = Payment.objects.create(
            order=order,
            method='card',
            status='pending',
            transaction_id='TXN-123456',
            amount=5000
        )
        assert payment.order == order
        assert payment.method == 'card'
        assert payment.amount == 5000

    def test_payment_unique_order(self, order):
        """
        Уникальность связи с заказом (OneToOneField)
        Ожидаемый результат: нельзя создать два платежа для одного заказа
        """
        Payment.objects.create(order=order, method='card', amount=5000)
        with pytest.raises(IntegrityError):
            Payment.objects.create(order=order, method='cash', amount=5000)

    def test_payment_amount_validation(self, order):
        """
        Валидация суммы платежа
        Ожидаемый результат: сумма не может быть отрицательной
        """
        with pytest.raises(ValidationError):
            payment = Payment(order=order, method='card', amount=-100)
            payment.full_clean()

    def test_payment_str_method(self, order):
        """
        Строковое представление платежа
        Ожидаемый результат: __str__ возвращает "Платёж для {order.order_number}"
        """
        payment = Payment.objects.create(order=order, method='card', amount=5000)
        assert str(payment) == f"Платёж для {order.order_number}"

    def test_payment_on_delete_protect(self, order):
        """
        Защита от удаления заказа с платежом
        Ожидаемый результат: нельзя удалить заказ, к которому привязан платеж
        """
        Payment.objects.create(order=order, method='card', amount=5000)
        with pytest.raises(IntegrityError):
            order.delete()

    def test_payment_status_transition(self, order):
        """
        Изменение статуса платежа
        Ожидаемый результат: статус можно менять
        """
        payment = Payment.objects.create(order=order, method='card', status='pending', amount=5000)
        assert payment.status == 'pending'

        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.save()
        assert payment.status == 'completed'
        assert payment.paid_at is not None