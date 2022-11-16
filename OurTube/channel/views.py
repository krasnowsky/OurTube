from account.models import User
from knox.auth import TokenAuthentication
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Channel
from .serializers import ChannelFilterSerializer, ChannelSerializer


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
        serializer = ChannelFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        user = User.objects.get(pk=request.user.id)
        channel = Channel.objects.filter(name=data['channel_name']).first()
        if not channel:
            channel = Channel.objects.create(
                name=data['channel_name'],
                external_id=data['external_id']
            )
        elif user.has_channel(channel):
            return Response('Channel already added', status=status.HTTP_200_OK)
        serializer = ChannelSerializer(channel)
        user.channels.add(serializer.data['id'])
        return Response('Successfully added channel', status=status.HTTP_200_OK)

class ChannelFilter(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # filter channels for adding to user's account
    def post(self, request):
        channel_name = request.data.get('channel_name')
        if not channel_name:
            return Response({'channel_name': 'This field is required.'})
        channels = Channel.objects.filter(name__icontains=channel_name)
        serializer = ChannelSerializer(channels, many=True)
        if not serializer.data:
            # if channel is not in the db, get it from yt api
            return Response('getting data from yt')
        return Response(serializer.data)

class ChannelRemove(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # remove channel from user's account
    def post(self, request):
        channel_name = request.data.get('channel_name')
        if not channel_name:
            return Response({'channel_name': 'This field is required.'})
        channel = Channel.objects.filter(name=channel_name).first()
        if not channel:
            return Response('This channel does not exists')
        if not request.user.has_channel(channel):
            return Response(f'{channel.name} is not on your list')
        request.user.channels.remove(channel)
        return Response(f'Successfully removed {channel.name}')
