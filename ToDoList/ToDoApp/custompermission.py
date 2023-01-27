from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


# Do profilu
class IsCurrentUserProfileOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = Options, Head, GET
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (obj.user == request.user) or IsAdminUser


# Do usera
class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = Options, Head, GET
        return (obj.id == request.user.id) or IsAdminUser


# Do pokoju
class IsCurrentUserCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = Options, Head, GET
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (obj.creator == request.user) or IsAdminUser
