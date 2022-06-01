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
