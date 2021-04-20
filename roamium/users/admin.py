from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users import models


class UserAdmin(BaseUserAdmin):
    ordering = ('email', 'first_name', 'last_name')
    list_display = ('email', 'first_name', 'last_name')
    fieldsets = (
        (('User Credentials'), {'fields': ('email', 'password')}),
        (('User Information'), {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        },),
    )


admin.site.register(models.User, UserAdmin)
