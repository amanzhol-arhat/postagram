from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # Суперпользователь может ВСЁ
        if request.user and request.user.is_superuser:
            return True

        # Разрешить всем читать (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Для создания/изменения/удаления нужна аутентификация
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Суперпользователь может ВСЁ с объектами
        if request.user and request.user.is_superuser:
            return True

        # Разрешить всем читать объекты
        if request.method in SAFE_METHODS:
            return True

        # Для изменений (PUT, PATCH, DELETE) разрешить только автору
        if hasattr(obj, 'author'):
            return obj.author == request.user

        # Если у объекта нет автора, разрешить аутентифицированным пользователям
        return request.user and request.user.is_authenticated