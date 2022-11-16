from django.urls import path

from .views import ChannelFilter, ChannelRemove, ChannelViewSet

urlpatterns = [
    path('', ChannelViewSet.as_view(), name='get-channels'),
    path('add/', ChannelViewSet.as_view(), name='add-channel'),
    path('filter/', ChannelFilter.as_view(), name='filter-channels'),
    path('remove/', ChannelRemove.as_view(), name='remove-channel'),
]
