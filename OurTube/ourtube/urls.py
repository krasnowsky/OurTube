from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework'
    )),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('channels/', include('channel.urls')),
    path('videos/', include('videos.urls')),
]
