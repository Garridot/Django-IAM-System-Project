from django.contrib import admin
from .models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff', 'roles')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
    search_fields = ('name',)

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'role', 'display_permissions')
    search_fields = ('user__email', 'role__name')
    list_filter = ('role',)

    def display_permissions(self, obj):
        return ', '.join([str(permission) for permission in obj.permissions.all()])
    display_permissions.short_description = 'Permissions'

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'action', 'timestamp')
    search_fields = ('user__email', 'action')
    list_filter = ('action', 'timestamp')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(AuditLog, AuditLogAdmin)