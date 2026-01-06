from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 1. Регистрация доступна всем (даже анонимам)
        if view.basename == "register":
            return True

        # 2. Анонимы могут только читать (GET), если это разрешено
        if request.method in SAFE_METHODS:
            return True

        # 3. Всё остальное (создать пост, лайкнуть, изменить) — только авторизованным
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # 1. Суперюзер может всё
        if request.user.is_superuser:
            return True

        # 2. Читать (GET) могут все
        if request.method in SAFE_METHODS:
            return True

        # 3. Действия взаимодействия (Лайк, Подписка)
        # Разрешаем любому авторизованному юзеру взаимодействовать с объектом
        if view.action in [
            "follow",
            "like",
            "remove_like",
            "like_comment",
            "remove_like_comment",
        ]:
            return True

        # 4. УНИВЕРСАЛЬНАЯ ПРОВЕРКА ВЛАДЕЛЬЦА
        # Если объект - это сам Пользователь (редактирует профиль)
        if obj == request.user:
            return True

        # Если у объекта есть атрибут 'author' (Пост, Комментарий) и он равен юзеру
        if hasattr(obj, "author"):
            return obj.author == request.user

        # Если ничего не подошло — запрещаем
        return False
