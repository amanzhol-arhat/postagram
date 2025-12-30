from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 1. Суперпользователь может всё
        if request.user and request.user.is_superuser:
            return True

        # 2. Разрешить всем просмотр (список постов и детали поста)
        if request.method in SAFE_METHODS:
            return True

        # 3. Для создания поста и лайков нужна авторизация
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 1. Суперпользователь — полный доступ
        if request.user and request.user.is_superuser:
            return True

        # 2. Читать объект (GET) могут все, даже анонимы
        if request.method in SAFE_METHODS:
            return True

        # 3. ЛОГИКА ДЛЯ ЛАЙКОВ:
        # Проверяем, что экшен называется 'like' или 'remove_like'
        # В этом случае нам важно только, чтобы пользователь был залогинен
        if view.action in ["like", "remove_like"]:
            return request.user.is_authenticated

        # 4. ЛОГИКА ДЛЯ ИЗМЕНЕНИЯ (PUT, PATCH, DELETE):
        # Если это не лайк и не GET, значит пользователь хочет изменить объект.
        # Если у объекта есть автор, сверяем с request.user
        if hasattr(obj, "author"):
            return obj.author == request.user

        # Если это объект пользователя, то сверяем его с request.user
        if isinstance(obj, get_user_model()):
            return obj == request.user

        return False
