from django.contrib import admin
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomUserAdmin(UserAdmin):
    # Используем нашу форму с email

    # Указываем сортировку и поля без упоминания username
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'gender', 'avatar', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Перерегистрируем модель
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)