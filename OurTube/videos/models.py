from django.db import models

from channel.models import Channel


class Video(models.Model):
    title = models.CharField(max_length=30)
    external_id = models.CharField(max_length=30)
    url = models.CharField(max_length=30)
    thumbnail_url = models.CharField(max_length=30)
    publish_date = models.CharField(max_length=30)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
