from django.db import models

import datetime
from django.utils import timezone


class UserRole(models.Model):
    ADMIN = 'ADMINISTRATOR'  # can do everything
    MODER = 'MODERATOR'      # like admin but less
    USER = 'USER'            # authorized user
    VIEWER = 'VIEWER'        # not authorized user

    USER_CHOICES = (
        (ADMIN, 'Administrator'),
        (MODER, 'Moderator'),
        (USER, 'User'),
        (VIEWER, 'Viewer'),
    )

    user_role = models.CharField(max_length=15,
                                 choices=USER_CHOICES,
                                 default=VIEWER)

    def __str__(self):
        return self.user_role


class IssueSeverity(models.Model):
    BLOCK = 'BLOCKER'  # cause of product failure
    CRIT = 'CRITICAL'  # cause of partial product failure
    MAJOR = 'MAJOR'    # some of the main logic works incorrectly
    MINOR = 'MINOR'    # doesn't break logic
    TRIV = 'TRIVIAL'   # doesn't affect the overall quality of product

    SEVERITY_CHOICES = (
        (BLOCK, 'Blocker'),
        (CRIT, 'Critical'),
        (MAJOR, 'Major'),
        (MINOR, 'Minor'),
        (TRIV, 'Trivial'),
    )

    issue_severity = models.CharField(max_length=9,
                                      choices=SEVERITY_CHOICES,
                                      null=True,
                                      default=TRIV)

    def __str__(self):
        return self.issue_severity


class IssuePriority(models.Model):
    HIGHEST = 'HIGHEST'  # will block progress
    HIGH = 'HIGH'        # could block progress
    MEDIUM = 'MEDIUM'    # potential to affect progress
    LOW = 'LOW'          # easily worked around
    LOWEST = 'LOWEST'    # little or no impact on progress

    PRIORITY_CHOICES = (
        (HIGHEST, 'Highest'),
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
        (LOWEST, 'Lowest'),
    )

    issue_rank = models.CharField(max_length=8,
                                  choices=PRIORITY_CHOICES,
                                  default=MEDIUM)

    def __str__(self):
        return self.issue_rank


class IssueType(models.Model):
    BUG = 'BUG'              # impairs or prevents the functions of a product
    EPIC = 'EPIC'            # group bugs and tasks, needs to be broken down
    IMPROVE = 'IMPROVEMENT'  # improvement of product functions
    FEATURE = 'FEATURE'      # new capability or feature
    TASK = 'TASK'            # work that needs to be done
    SUBTASK = 'SUBTASK'      # work that is required to complete a task

    TYPE_CHOICES = (
        (BUG, 'Bug'),
        (EPIC, 'Epic'),
        (IMPROVE, 'Improvement'),
        (FEATURE, 'New Feature'),
        (TASK, 'Task'),
        (SUBTASK, 'Sub-task'),
    )

    issue_type = models.CharField(max_length=12,
                                  choices=TYPE_CHOICES,
                                  default=TASK)

    def __str__(self):
        return self.issue_type


class IssueStatus(models.Model):
    OPEN = 'OPEN'            # issue is open and ready for the assignee to start work on it
    PROGRESS = 'PROGRESS'    # issue is being actively worked on at the moment by the assignee
    DONE = 'DONE'            # work has finished
    TODO = 'TODO'            # issue has been reported and is waiting for the team to action it
    REVIEW = 'REVIEW'        # assignee has carried out the work needed and it needs peer review
    APPROVED = 'APPROVED'    # reviewer has approved work completed
    REJECTED = 'REJECTED'    # reviewer has rejected the work completed
    CANCELLED = 'CANCELLED'  # work has stopped and issue is considered done

    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (TODO, 'To Do'),
        (REVIEW, 'In Review'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    )

    issue_status = models.CharField(max_length=10,
                                    choices=STATUS_CHOICES,
                                    default=TODO)

    def __str__(self):
        return self.issue_status


class AccessType(models.Model):
    GUEST = 'GUEST'          # random person not from the project
    DEV = 'DEVELOPER'        # developer of the project
    MAINTAIN = 'MAINTAINER'  # maintain the project
    OWNER = 'OWNER'          # own the project

    ACCESS_TYPE = (
        (GUEST, 'Guest'),
        (DEV, 'Developer'),
        (MAINTAIN, 'Maintainer'),
        (OWNER, 'Owner'),
    )

    access_type = models.CharField(max_length=11,
                                   choices=ACCESS_TYPE,
                                   default=GUEST)

    def __str__(self):
        return self.access_type


class UserProfile(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=95)
    allow_email_notification = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='photos/%Y/%m/%d/')
    user_role = models.ForeignKey(UserRole, models.SET_NULL, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.username, self.email_address)


class Project(models.Model):
    project_name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.project_name


class ProjectAccess(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    access_type = models.ForeignKey(AccessType, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.project, self.user, self.access_type)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reporter = models.ForeignKey(UserProfile, models.SET_NULL, null=True)
    issue_type = models.ForeignKey(IssueType, models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    added_date = models.DateTimeField(auto_now_add=True)
    time_estimate = models.DurationField()
    due_date = models.DateTimeField()
    date_submitted = models.DateTimeField(null=True, default=None)
    last_change = models.DateTimeField(default=timezone.now)
    issue_priority = models.ForeignKey(IssuePriority, models.SET_NULL, null=True)
    issue_status = models.ForeignKey(IssueStatus, models.SET_NULL, null=True)
    issue_severity = models.ForeignKey(IssueSeverity, models.SET_NULL, null=True)

    def __str__(self):
        return self.title


# class RelatedIssue(models.Model):
#     source_issue = models.ForeignKey(Issue, related_name=, on_delete=models.CASCADE)
#     destination_issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{} to {}'.format(self.source_issue, self.destination_issue)


class IssueAssignee(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return '{} assignee to {}'.format(self.user, self.issue)


class IssueNote(models.Model):
    title = models.CharField(max_length=120)
    note_text = models.TextField()
    note_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, models.SET_NULL, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return '{} wrote {} to {}'.format(self.user, self.title, self.issue)
