from rest_framework.test import APITestCase
from django.urls import reverse

class UserAuthenticateMixin(APITestCase):
    def setUp(self):
        self.username = 'test_username'
        self.email = 'test@email.com'
        self.password = 'test_password'
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        self.client.post(self.register_url, data)
        data = {
            'username': self.username,
            'password': self.password   
        }
        response = self.client.post(self.login_url, data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])