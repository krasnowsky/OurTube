# Generated by Django 4.1.3 on 2022-11-19 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='thumbnail_url',
            field=models.CharField(default='url', max_length=30),
            preserve_default=False,
        ),
    ]