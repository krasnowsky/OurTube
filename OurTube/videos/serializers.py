from .models import Video
from rest_framework import serializers


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'external_id', 'url', 'thumbnail_url', 'publish_date', 'channel_id']


class VideoGetSerializer(serializers.Serializer):
    video_id = serializers.IntegerField()
    url_only = serializers.BooleanField()
