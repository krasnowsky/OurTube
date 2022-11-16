from django.urls import path
from .views import ChannelViewSet, ChannelFilter, ChannelRemove

urlpatterns = [
    path('', ChannelViewSet.as_view(), name='get-channels'),
    path('add/', ChannelViewSet.as_view(), name='add-channel'),
    path('filter/', ChannelFilter.as_view(), name='filter-channels'),
    path('remove/', ChannelRemove.as_view(), name='remove-channel'),
]