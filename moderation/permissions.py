from rest_framework import permissions

class IsBlockedUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        return not request.user.blocked