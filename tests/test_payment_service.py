from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import Mock, patch

from game.services.payment_service import create_payment, check_payment_status
from game.models import Transaction

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class PaymentServiceTests(TestCase):
    @patch('game.services.payment_service.paynow')
    def test_create_payment_success(self, mock_paynow):
        payment_obj = Mock()
        payment_obj.reference = 'ref123'
        payment_obj.add = Mock()
        mock_paynow.create_payment.return_value = payment_obj
        mock_response = Mock(success=True, redirect_url='http://pay', poll_url='http://poll')
        mock_paynow.send.return_value = mock_response

        result = create_payment('test@example.com', 10)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['redirect_url'], 'http://pay')
        self.assertEqual(Transaction.objects.count(), 1)

    @patch('requests.get')
    def test_check_payment_status(self, mock_get):
        mock_get.return_value = Mock(status_code=200, text='status=Paid&reference=test%40example.com&amount=10&paynowreference=xyz')
        result = check_payment_status('http://poll')
        self.assertEqual(result['status'], 'Paid')
        self.assertEqual(result['email'], 'test@example.com')
        self.assertEqual(result['amount'], '10')
        self.assertEqual(result['paynow_reference'], 'xyz')

