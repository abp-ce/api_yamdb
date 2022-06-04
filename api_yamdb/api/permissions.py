from rest_framework import permissions
from reviews.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение позволяющее добавлять/редактировать/удалять его только
     пользователю с ролью ADMIN. Остальные имеют доступ на чтение.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and request.user.role == User.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and request.user.role == User.ADMIN
        )


class IsAdminRoleOnly(permissions.BasePermission):
    """
    Разрешение позволяющее добавлять/редактировать/удалять его только
     пользователю superuser или с ролью ADMIN. Остальные не имеют доступа.
    """
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.role == User.ADMIN)
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_authenticated and request.user.role == User.ADMIN)
            or request.user.username == obj.username
            or request.user.is_superuser
        )
