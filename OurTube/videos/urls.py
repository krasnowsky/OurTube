from django.urls import path

from .views import VideoByChannelView, VideoView

urlpatterns = [
    path('from-channels/', VideoByChannelView.as_view(), name='video-channel'),
    path('', VideoView.as_view(), name='video'),
]
