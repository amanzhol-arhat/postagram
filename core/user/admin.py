from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Custom fields', {'fields': ('bio', 'avatar', 'post_liked', 'comments_liked', 'avatar_seed')}),
    )
    
    readonly_fields = ('last_login', 'created_at', 'updated_at')
