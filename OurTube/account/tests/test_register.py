from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from account.models import User

class RegisterTest(APITestCase):
    def setUp(self):
        self.username = 'test_username'
        self.email = 'test@email.com'
        self.password = 'test_password'
        self.url = reverse('register')

    def test_registration_no_data(self):
        # Arrange
        expected_response = {
            'username': ['This field is required.'],
            'password': ['This field is required.']
        }
        data = {}
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_incomplete_data(self):
        # Arrange
        expected_response = {
            'password': ['This field is required.']
        }
        data = {'username': 'test_username'}
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_successful(self):
        # Arrange
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['token'])
        self.assertEqual(response.json()['user']['username'], self.username)
        self.assertEqual(response.json()['user']['email'], self.email)
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)