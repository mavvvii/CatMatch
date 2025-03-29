from django.test import TestCase
from user.models import User
from django.urls import reverse
from user.views.user_view import BaseAPISet
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

class TestUser(TestCase):
    def setUp(self):
        User.objects.create_user(username='admin', password='<PASSWORD>')
        User.objects.create_user(username='user', password='<PASSWORD>')

    # Test successful
    def test_user(self):
        username = User.objects.get(username='user')
        self.assertEqual(username.get_name(), 'user')


class UserEndpointTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='alice', email='alice@example.com', password='testpassword')
        User.objects.create_user(username='bob', email='bob@example.com', password='testpassword')

    def test_user_list(self):
        response = self.client.get('/users/test3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class BaseAPISetThrottleTest(APITestCase):
    def setUp(self):
        self.view = BaseAPISet()
        self.view.action = 'retrieve'

        # Tworzymy użytkownika
        self.user = User.objects.create_user(username='test', password='test123')

        # Tworzymy request
        factory = APIRequestFactory()
        self.request = factory.get('/fake-url/')
        self.request.user = self.user  # Dodajemy usera do requesta

        self.view.request = self.request

    def test_get_throttles(self):
        print('throttle_scope:', self.view.throttle_scope)
        throttles = self.view.get_throttles()
        print('throttle_scope:', self.view.throttle_scope)
        for t in throttles:
            t.allow_request(self.request, self.view)  # Tutaj ustawiamy throttle_scope

        print('🚀 Throttles:', throttles)
        print('🔍 Throttle Scopes:', [t.scope for t in throttles])