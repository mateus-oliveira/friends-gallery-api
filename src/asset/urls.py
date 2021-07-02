from django.urls import path, include
from rest_framework import routers

from .views import AssetViewSet

router = routers.DefaultRouter()
router.register('assets', AssetViewSet, basename='assets')

urlpatterns = [
    path("",  include((router.urls, 'asset'), namespace='asset_urls')),
]
