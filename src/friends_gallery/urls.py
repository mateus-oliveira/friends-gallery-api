
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

# admin.autodiscover()
# admin.site.enable_nav_sidebar = False


urlpatterns = [
    path('asset/', include('asset.urls')),
    path('authentication/', include('authentication.urls')),
    path('posts/', include('posts.urls')),

    path('admin/', admin.site.urls),
    path('drf/', include('rest_framework.urls')),
]

if environment == 'LOCAL':
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
