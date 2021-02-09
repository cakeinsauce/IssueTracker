from django.contrib import admin

from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email_address', 'first_name',
                    'last_name', 'date_created', 'user_role', 'enabled')
    list_display_links = ('id', 'username')
    list_editable = ('enabled',)
    search_fields = ('username', 'email_address')
    list_filter = ('user_role', 'enabled')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'title', 'reporter', 'added_date', 'due_date', 'issue_type')
    list_display_links = ('id', 'title')
    search_fields = ('project', 'title', 'reporter', 'issue_type')
    list_filter = ('issue_type',)


class IssueAssigneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'issue')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'issue')
    list_filter = ('issue',)


class IssueNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'note_date', 'user', 'issue')
    list_display_links = ('id', 'title')
    search_fields = ('user', 'issue')
    list_filter = ('note_date', 'issue')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name')
    list_display_links = ('id', 'project_name')
    search_fields = ('project_name',)


class ProjectAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'user', 'access_type')
    list_display_links = ('id', 'project')
    search_fields = ('project', 'user')
    list_filter = ('project', 'user', 'access_type')


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


models = [UserProfile, Issue, IssueAssignee, IssueNote, Project, ProjectAccess, UserRole,
          IssueSeverity, IssuePriority, IssueType, IssueStatus, AccessType]

models_admin = [UserProfileAdmin, IssueAdmin, IssueAssigneeAdmin, IssueNoteAdmin,
                ProjectAdmin, ProjectAccessAdmin, UserRoleAdmin, IssueSeverityAdmin,
                IssuePriorityAdmin, IssueTypeAdmin, IssueStatusAdmin, AccessTypeAdmin]

for model, model_admin in zip(models, models_admin):
    admin.site.register(model, model_admin)
