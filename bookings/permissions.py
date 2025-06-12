from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        print("request.user",request.user)
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):

        if request.user.role == 'ADMIN':
            return True
        return obj.user == request.user