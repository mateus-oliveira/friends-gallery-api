from django.urls import reverse
from rest_framework import permissions


class PostPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        if request.stream.path == reverse("post_urls:posts-like", args=[obj.id]):
            return request.user.is_authenticated

        if request.stream.path == reverse("post_urls:posts-to-approve", args=[obj.id]):
            return request.user.role == 1

        return request.user == obj.user


class CommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user
