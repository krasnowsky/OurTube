from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

class LoginTest(APITestCase):
    def setUp(self):
        self.username = 'test_username'
        self.email = 'test@email.com'
        self.password = 'test_password'
        self.login_url = reverse('login')
        self.register_url = reverse('register')

    def _register_user(self):
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        self.client.post(self.register_url, data)

    def test_login_no_data(self):
        # Arrange
        data = {}
        expected_response = {
            'username': ['This field is required.'],
            'password':['This field is required.']
        }
        # Act
        response = self.client.post(self.login_url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_wrong_password(self):
        # Arrange
        self._register_user()
        data = {
            'username': self.username,
            'password': 'wrong_password'
        }
        expected_response = {
            'non_field_errors': [
                'Unable to log in with provided credentials.'
            ]
        }
        # Act
        response = self.client.post(self.login_url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_wrong_username(self):
        # Arrange
        self._register_user()
        data = {
            'username': 'wrong_username',
            'password': self.password
        }
        expected_response = {
            'non_field_errors': [
                'Unable to log in with provided credentials.'
            ]
        }
        # Act
        response = self.client.post(self.login_url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_successful(self):
        # Arrange
        self._register_user()
        data = {
            'username': self.username,
            'password': self.password
        }
        # Act
        response = self.client.post(self.login_url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['token'])

    def test_logout_successful(self):
        # Arrange
        self._register_user()
        logout_url = reverse('logout')
        data = {
            'username': self.username,
            'password': self.password
        }
        login_response = self.client.post(self.login_url, data)
        token = login_response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # Act
        response = self.client.post(logout_url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
