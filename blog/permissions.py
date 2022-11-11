from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # elif request.user and request.user.is_authenticated:
        #     return bool(request.user and request.user.is_authenticated)
        # else:
        #     return bool(request.user and request.user.is_authenticated)
        return request.user == obj.author


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
 