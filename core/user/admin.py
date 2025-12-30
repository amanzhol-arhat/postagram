from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserFollow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """

    # 1. Исправил created -> created_at
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "created_at",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")

    # 2. Исправил ordering
    ordering = ("created_at",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        # 3. Исправил created -> created_at и updated -> updated_at
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
        (
            "Custom fields",
            {
                "fields": (
                    "bio",
                    "avatar",
                    "posts_liked",
                    "comments_liked",
                    "avatar_seed",
                )
            },
        ),
    )

    # 4. Исправил readonly_fields
    readonly_fields = ("last_login", "created_at", "updated_at")


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """
    Панель для просмотра кто на кого подписан
    """

    list_display = ("user", "followed", "created_at")
    search_fields = ("user__username", "followed__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
