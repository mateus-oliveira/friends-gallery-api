
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import (
    environment,
    MEDIA_ROOT,
    MEDIA_URL,
    STATIC_ROOT,
    STATIC_URL,
)


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('drf/', include('rest_framework.urls')),
]

if environment == 'DEVELOPMENT':
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
