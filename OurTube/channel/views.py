from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from videos.api import YouTubeAPI as api

from .models import Channel
from .serializers import ChannelSerializer


class ChannelViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # get data to view for the user
    def get(self, request):
        channels = request.user.channels.all()
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)

    # add channel to user's account
    def post(self, request):
        data = request.data
        user = request.user
        channel = Channel.objects.filter(external_id=data['external_id']).first()
        if not channel:
            channel = Channel.objects.create(
                name=data['channel_name'],
                external_id=data['external_id'],
                thumbnail_url=data['thumbnail_url']
            )
            videos = api.get_videos_from_channel(data['external_id'], channel)
        elif user.has_channel(channel):
            return Response('Channel already added', status=status.HTTP_200_OK)
        serializer = ChannelSerializer(channel)
        user.channels.add(serializer.data['id'])
        return Response(
            'Successfully added channel',
            status=status.HTTP_200_OK
        )


# filter channels for adding to user's account
class ChannelFilter(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        channel_name = request.data.get('channel_name')
        if not channel_name:
            return Response({'channel_name': 'This field is required.'})
        final = []
        channels = Channel.objects.exclude(
            id__in=request.user.get_channels_ids()
        ).filter(name__icontains=channel_name)
        serializer = ChannelSerializer(channels, many=True)
        if len(channels) <= 2:
            api_response = api.get_channels_by_name(channel_name)
            merged = serializer.data + api_response
            final = list({v['external_id']: v for v in merged}.values())
        return Response(final)


# remove channel from user's account
class ChannelRemove(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        external_id = request.data.get('external_id')
        channel = Channel.objects.filter(external_id=external_id).first()
        request.user.channels.remove(channel)
        return Response(f'Successfully removed {channel.name}')
