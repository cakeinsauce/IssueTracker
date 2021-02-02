from django.contrib import admin

from .models import UserProfile, UserRole


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email_address', 'first_name',
                    'last_name', 'date_created', 'user_role', 'enabled')
    list_display_links = ('id', 'username')
    list_editable = ('enabled',)
    search_fields = ('username', 'email_address')
    list_filter = ('user_role', 'enabled')


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_role')
    list_display_links = ('id', 'user_role')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
