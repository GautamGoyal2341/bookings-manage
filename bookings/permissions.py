from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        print("request.user",request.user)
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'
