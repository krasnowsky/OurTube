from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VideoSerializer, VideoGetSerializer
from .models import Video


class VideoByChannelView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # assuming that channel exsists and user has such channel
    def get(self, request):
        external_id = request.data.get('external_id')
        if not external_id:
            user_channels = request.user.channels.all()
            all_videos = Video.objects.filter(
                channel__in=user_channels).order_by('-publish_date')
            serializer = VideoSerializer(all_videos, many=True)
            return Response(serializer.data)
        single_channel_videos = Video.objects.filter(
            channel__external_id=external_id
        )
        # here yt api should be asked if last video is older then 24h
        if not single_channel_videos:
            return Response('No videos found for this channel.')
        videos = VideoSerializer(single_channel_videos, many=True)
        return Response(videos.data)


class VideoView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = VideoGetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        video_id = serializer.validated_data['video_id']
        url_only = serializer.validated_data['url_only']
        video = Video.objects.filter(pk=video_id).first()
        serializer = VideoSerializer(video)
        if url_only:
            return Response(serializer.data['url'])
        return Response(serializer.data)
