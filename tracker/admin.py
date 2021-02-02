from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email_address', 'first_name',
                    'last_name', 'date_created', 'user_role', 'enabled')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email_address')


admin.site.register(UserProfile, UserProfileAdmin)
