from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path("",  include((router.urls, 'posts'), namespace='posts_urls')),
]
