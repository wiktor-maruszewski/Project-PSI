from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = Options. Head, Get
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user
