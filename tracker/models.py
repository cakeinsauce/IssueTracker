from django.db import models

import datetime
from django.utils import timezone


class UserRole(models.Model):
    ADMIN = 'ADMINISTRATOR'  # can do everything
    MODER = 'MODERATOR'  # like admin but less
    USER = 'USER'  # authorized user
    VIEWER = 'VIEWER'  # not authorized user

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



