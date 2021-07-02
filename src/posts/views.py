from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import (
    PostCreateSerializer, PostSerializer, CommentSerializer,
)
from .permissions import CommentPermissions, PostPermissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]
    filterset_fields = ['user']

    def create(self, request, *args, **kwargs):
        self.serializer_class = PostCreateSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, pk=None):
        try:
            post = self.get_object()
            if request.user in post.like:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            post.save()

            return Response(
                data=PostSerializer(instance=post).data,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise ValidationError('Error when trying like a post!')

    @action(methods=['POST'], detail=True, url_path='to-approve')
    def to_approve(self, request, pk=None):
        try:
            post = self.get_object()
            post.status = request.data["status"]
            post.save()

            return Response(
                data=PostSerializer(instance=post).data,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise ValidationError('Error when trying to approve a post!')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]
    filterset_fields = ['user', 'post']
