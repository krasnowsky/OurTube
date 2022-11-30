from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=30)
    external_id = models.CharField(max_length=30)
    thumbnail_url = models.CharField(max_length=30)

    def __str__(self):
        return self.name
