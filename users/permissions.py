from rest_framework import permissions

from users.models import STADIONADMIN


class StadionAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == STADIONADMIN
