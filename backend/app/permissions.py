from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsSuperUserOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_superuser or obj == request.user)
    
class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.method in SAFE_METHODS)

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_organizer or request.user.is_superuser)
    
class IsOrganizerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_organizer or request.user.is_superuser or request.method in SAFE_METHODS)
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user