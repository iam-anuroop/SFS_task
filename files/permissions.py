from rest_framework.permissions import BasePermission

class IsopsUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.role  == 'ops'