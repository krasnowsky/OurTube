from rest_framework import serializers

from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    external_id = serializers.CharField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'external_id']


class ChannelFilterSerializer(serializers.Serializer):
    channel_name = serializers.CharField(required=True)
    external_id = serializers.CharField(required=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'external_id']
