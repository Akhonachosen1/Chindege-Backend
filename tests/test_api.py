from django.urls import reverse
from rest_framework.test import APITestCase
from django.test.utils import override_settings

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class AuthAPITests(APITestCase):
    def test_register_login_and_start_game(self):
        reg_url = reverse('register_user')
        data = {'username': 'tester', 'password': 'testpass123'}
        response = self.client.post(reg_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

        login_url = reverse('login_user')
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        start_url = reverse('start_game')
        response = self.client.post(start_url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('crash_point', response.data)

