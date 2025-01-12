from django.test import TestCase
from user.models import User
from django.urls import reverse


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