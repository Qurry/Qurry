import json

from django.urls import reverse_lazy
from qurry_api.tests import AuthenticatedTestCase

from .models import ActivationToken, User


class LoginTestCase(AuthenticatedTestCase):
    def can_login(self, email, password):
        self.login(email, password, enforce_success=False)
        return self.access_token is not None

    def test_valid_login(self):
        self.assertTrue(self.can_login('admin@hpi.de', 'admin'))
        self.assertTrue(self.can_login('admin@uni-potsdam.hpi.de', 'admin'))
        self.assertTrue(self.can_login('ADMIN@HPI.DE', 'admin'))

    def test_invalid_login(self):
        self.assertFalse(self.can_login('admin@hpi.de', 'admi'))
        self.assertFalse(self.can_login('admin@hpi.de', ''))
        self.assertFalse(self.can_login('test@hpi.de', 'test'))
        self.assertFalse(self.can_login('', ''))

    def successfully_registered(self, email, username, password):
        response = self.request('POST', reverse_lazy('register'),
                                {'email': email, 'username': username, 'password': password}, json=False)
        return response.status_code == 201

    def register_and_return_activation_url(self, email, username, password):
        self.assertTrue(self.successfully_registered(
            email, username, password))
        activation_token = ActivationToken.objects.get(user__username=username)
        token = activation_token.token
        uid = activation_token.user.id

        return reverse_lazy('activate-account',
                            kwargs={'uid': uid, 'token': token})

    def test_valid_register(self):
        self.assertTrue(self.successfully_registered(
            'register1@hpi.de', 'register1', 'includeI09.'))

        self.assertTrue(self.successfully_registered(
            'register2@student.hpi.de', 'register2', 'includeI09.'))

        self.assertTrue(self.successfully_registered(
            'register3@student.uni-potsdam.hpi.de', 'register3', 'includeI09.'))

    def test_register_and_activation(self):
        activation_url = self.register_and_return_activation_url(
            'register@student.uni-potsdam.hpi.de', 'register', 'includeI09.')
        self.assertFalse(self.can_login(
            'register@student.uni-potsdam.hpi.de', 'includeI09.'))

        response = self.client.get(activation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.can_login(
            'register@student.uni-potsdam.hpi.de', 'includeI09.'))
        self.assertTrue(self.can_login(
            'register@student.hpi.de', 'includeI09.'))

    def test_invalid_register(self):
        self.assertFalse(self.successfully_registered(
            'new@hhpi.de', 'new', 'includeI09.'))
        self.assertFalse(self.successfully_registered(
            'admin@hpi.de', 'new', 'includeI09.'))
        self.assertFalse(self.successfully_registered(
            'new@hpi.de', 'admin', 'inclueI9.'))
        self.assertFalse(self.successfully_registered(
            'new@hpi.de', '', 'includeI09.'))
        self.assertFalse(self.successfully_registered(
            '', 'new', 'includeI09.'))
        # bad passwords
        self.assertFalse(self.successfully_registered(
            'new@hpi.de', 'new', 'SHORT'))


class UsersTestCase(AuthenticatedTestCase):
    def test_permissions(self):
        self.assertEqual(self.request('GET', reverse_lazy(
            'view-users')).status_code, 401)

        self.assertEqual(self.request('GET', reverse_lazy(
            'view-users'), authenticated=True).status_code, 200)

        self.assertEqual(self.request('GET', reverse_lazy(
            'view-profile')).status_code, 401)

        self.assertEqual(self.request('GET', reverse_lazy(
            'view-profile'), authenticated=True).status_code, 200)

    def test_users_results(self):
        response = self.request('GET', reverse_lazy(
            'view-users'), authenticated=True)

        sample_data = json.loads(response.content)[0]
        sample_user = User.objects.get(id=sample_data['id'])

        self.assertEqual(sample_data, sample_user.as_detailed())

        response = self.request('GET', reverse_lazy(
            'view-user-details', args=[sample_user.id]), authenticated=True)

        sample_data = json.loads(response.content)
        self.assertEqual(sample_data, sample_user.as_detailed())

        response = self.request('GET', reverse_lazy(
            'view-user-details', args=['fake-id']), authenticated=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_results(self):
        response = self.request('GET', reverse_lazy(
            'view-profile'), authenticated=True)

        expected = User.objects.get(username='admin').profile_info()
        got = json.loads(response.content)

        self.assertEqual(expected, got)

    def test_user_editing(self):
        User.objects.get_or_create(username='test')

        response = self.request('PATCH', reverse_lazy(
            'view-profile'), {'username': 'ADMIN_ADMIN'}, authenticated=True)
        self.assertEqual(response.status_code, 200)
        assert not User.objects.filter(username='admin').exists()

        response = self.request('PATCH', reverse_lazy(
            'view-profile'), {'username': 'test'}, authenticated=True)
        self.assertEqual(response.status_code, 400)

        response = self.request('PATCH', reverse_lazy(
            'view-profile'), {'oldPassword': 'admin', 'newPassword': 'SHORT'}, authenticated=True)
        self.assertEqual(response.status_code, 400)

        response = self.request('PATCH', reverse_lazy(
            'view-profile'), {"oldPassword": "admin", "newPassword": "includeI09."}, authenticated=True)

        self.assertEqual(response.status_code, 200)
