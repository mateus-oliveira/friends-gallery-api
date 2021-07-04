from django.urls import path, include

from .views import public

urlpatterns = [
    path('', public, name='public'),
    path('asset/', include('asset.urls')),
    path('authentication/', include('authentication.urls')),
    path('post/', include('post.urls')),
]
