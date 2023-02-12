from rest_framework import status
from django.urls import reverse
import responses
from account.models import User
from account.mixins import UserAuthenticateMixin
from channel.models import Channel
from videos.utils import add_youtube_video_response


class GetChannelsTest(UserAuthenticateMixin):
    @responses.activate
    def test_get_channels(self):
        # Arrange
        expected_response = [
            {
                'id': 1,
                'name': 'test_channel_name',
                'external_id': 'test_external_id',
                'thumbnail_url': 'test_thumbnail_url',
            }
        ]
        add_youtube_video_response()
        url = reverse('add-channel')
        data = {
            'channel_name': 'test_channel_name',
            'external_id': 'test_external_id',
            'thumbnail_url': 'test_thumbnail_url',
        }
        self.client.post(url, data)
        url = reverse('get-channels')
        # Act
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    @responses.activate
    def test_get_channels_no_added(self):
        # Arrange
        expected_response = []
        add_youtube_video_response()
        url = reverse('get-channels')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)


class AddChannelsTest(UserAuthenticateMixin):
    @responses.activate
    def test_add_channels(self):
        # Arrange
        add_youtube_video_response()
        url = reverse('add-channel')
        data = {
            'channel_name': 'test_channel_name',
            'external_id': 'test_external_id',
            'thumbnail_url': 'test_thumbnail_url',
        }
        # Act
        response = self.client.post(url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), 'Successfully added channel')
        user = User.objects.prefetch_related('channels').first()
        channel = Channel.objects.get(name='test_channel_name')
        self.assertIn(channel.id, user.get_channels_ids())
        self.assertTrue(user.has_channel(channel))
