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


class Severity(models.Model):
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
    BUG = 'BUG'
    EPIC = 'EPIC'
    IMPROVE = 'IMPROVEMENT'
    FEATURE = 'FEATURE'
    TASK = 'TASK'
    SUBTASK = 'SUBTASK'

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


class UserProfile(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=95)
    allow_email_notification = models.BooleanField(default=False)
    last_online = models.DateTimeField()
    date_created = models.DateTimeField()
    picture_url = models.CharField(max_length=255)
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL)
    enabled = models.BooleanField(default=True)



