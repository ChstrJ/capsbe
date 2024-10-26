from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    
    def has_permission(self, request, view):
        try:
            if not request.user:
                raise PermissionDenied("User is not authenticated.")
        
            if request.user.user_type not in ['admin']:
                raise PermissionDenied("You do not have permission to access this resource.")
        except PermissionError as e:
            raise PermissionDenied("Authentication token is not provided.")
        return True
    
class IsResident(BasePermission):
    
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied("User is not authenticated.")
            
            if request.user.residents.verified == False:
                raise PermissionDenied("User is not verified")
        
        except PermissionError as e:
            raise PermissionDenied("Authentication token is not provided.")
                
        return True
