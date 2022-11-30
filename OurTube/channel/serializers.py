from rest_framework import serializers

from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    external_id = serializers.CharField()
    thumbnail_url = serializers.CharField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'external_id', 'thumbnail_url']
