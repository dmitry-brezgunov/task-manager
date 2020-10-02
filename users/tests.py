from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {'username': 'testuser', 'password': 'testpassword'}

    def test_registration(self):
        url = reverse('register')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_token(self):
        url = reverse('token')
        user = User.objects.create_user(
            username=self.data['username'], password=self.data['password'])
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.get().user, user)

    def test_permissions(self):
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
