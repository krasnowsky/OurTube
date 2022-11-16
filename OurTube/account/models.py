from django.contrib.auth.models import AbstractUser
from django.db import models
from channel.models import Channel

class User(AbstractUser):
    channels = models.ManyToManyField(Channel, related_name='channels')

    def has_channel(self, channel):
        return channel in self.channels.all()