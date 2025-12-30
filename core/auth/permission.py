from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 1. Регистрация доступна всем (даже анонимам)
        if view.action == "create":
            return True

        # 2. Список юзеров, подписки и сам профиль доступны авторизованным
        if view.action in ["list", "retrieve", "follow", "followers", "following"]:
            return bool(request.user and request.user.is_authenticated)

        # 3. Удаление и обновление (PATCH/DELETE) доступны авторизованным
        # (конкретная проверка "свой ли это аккаунт" будет в has_object_permission)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # 1. Суперпользователь может всё
        if request.user.is_superuser:
            return True

        # 2. Безопасные методы (просмотр профиля) разрешены всем авторизованным
        if request.method in SAFE_METHODS:
            return True

        # 3. !!! ИСПРАВЛЕНИЕ !!!
        # Разрешаем действие 'follow' (подписаться) на ЛЮБОГО юзера.
        # Логика "нельзя подписаться на себя" уже есть во ViewSet,
        # здесь мы просто разрешаем сам факт отправки запроса к чужому объекту.
        if view.action == "follow":
            return True

        # 4. Изменять (PATCH, DELETE) можно только СВОЙ профиль
        return obj == request.user
