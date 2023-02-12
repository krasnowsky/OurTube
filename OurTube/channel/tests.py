from django.test import TestCase, Client
from django.urls import reverse

from .models import Channel

class ChannelModelTestCase(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(name='test', external_id='123', thumbnail_url='random_url')

    def test_simple_test(self):
        self.assertEqual(1,1)

    def test_get_channels(self):
        # Arrange
        url = reverse('get-channels')
        response = self.client.get(url)

from rest_framework.test import APIClient
#from knox.serializers import User
from account.models import User

class SignInAPITests(TestCase):
    def test_sign_in(self):
        channel = Channel.objects.create(name='test', external_id='123', thumbnail_url='random_url')
        self.user = User.objects.create_user(
            username='test_user', 
            password='12345')
        self.user.channels.add(channel)
        self.client = APIClient()
        auth_url = reverse('login')
        res = self.client.post(auth_url,
            data=dict(username="test_user", 
            password="12345"))
        access_token = res.data["token"]
        self.assertIsNotNone(access_token)
        self.assertTrue(self.client.login(username='test_user', password='12345'))
        url = reverse('get-channels')
        response = self.client.get(url)
        self.assertEqual(1,1)
        