from django.urls import path
from .views import VideoByChannelView, VideoView

urlpatterns = [
    path('from-channels/', VideoByChannelView.as_view(), name='get-videos-from-channels'),
    path('', VideoView.as_view(), name='get-video'),
]