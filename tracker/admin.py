from django.contrib import admin

from .models import UserProfile, UserRole, IssueSeverity, IssuePriority, IssueType, IssueStatus, AccessType


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


class IssueSeverityAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_severity')
    list_display_links = ('id', 'issue_severity')


class IssuePriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_rank')
    list_display_links = ('id', 'issue_rank')


class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_type')
    list_display_links = ('id', 'issue_type')


class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_status')
    list_display_links = ('id', 'issue_status')


class AccessTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_type')
    list_display_links = ('id', 'access_type')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(IssueSeverity, IssueSeverityAdmin)
admin.site.register(IssuePriority, IssuePriorityAdmin)
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(AccessType, AccessTypeAdmin)
