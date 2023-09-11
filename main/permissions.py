from rest_framework import permissions

class ModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()
    
class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(name='moderator').exists()
        
        return obj.user == request.user or is_moderator