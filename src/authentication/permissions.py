from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj
