from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    message = 'Solo las autoridades pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
