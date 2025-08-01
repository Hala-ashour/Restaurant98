from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
   

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff



