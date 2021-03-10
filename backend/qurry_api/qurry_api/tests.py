import json

from django.conf import settings
from django.core.mail import send_mail
from django.test import Client, TestCase
from django.urls.base import reverse_lazy


class AuthenticatedTestCase(TestCase):
    fixtures = ['fixtures/testing.json']

    def setUp(self):
        self.client = Client()
        self.login_as_admin()

    def request(self, method, url, *args, authenticated=False, **kwargs):
        if authenticated:
            kwargs['HTTP_AUTHORIZATION'] = 'Bearer ' + self.access_token
        return getattr(self.client, method.lower())(url, *args, **kwargs)

    def login(self, email, password, enforce_success=True):
        response = self.client.post(reverse_lazy('login'), data=json.dumps(
            {'email': email, 'password': password}), content_type='application/json')

        if enforce_success:
            self.assertEqual(response.status_code, 200)

        if response.status_code == 200:
            response_body = json.loads(response.content)
            token = response_body.get('access')
            self.access_token = token
        else:
            self.access_token = None

    def login_as_admin(self):
        self.login('admin@hpi.de', 'admin')


class BaseTestCase(AuthenticatedTestCase):
    def test_emailing(self):
        send_mail('TEST', 'test message', settings.EMAIL_HOST_USER, [
            'admin@qurry.de'], html_message='test message')
