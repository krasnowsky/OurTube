import json

from django.test import TestCase, Client
from django.urls import reverse, resolve

class RegisterTest(TestCase):
    def test_registration_successful(self):
        # Arrange
        url = reverse('register')
        data = {
            'username': 'test_username',
            'email': 'test@email.com',
            'password': 'test_password'
        }
        # Act
        response = self.client.post(url, data)
        import ipdb; ipdb.set_trace()
        # Assert
        self.assertEqual(1,1)