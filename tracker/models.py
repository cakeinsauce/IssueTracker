from django.db import models

import datetime
from django.utils import timezone


def get_default_user_role():
    """ get a default value for user_role """
    return UserRole.objects.get(user_role='USER')


class UserProfile(models.Model):
    username = models.CharField(max_length=25, verbose_name='Имя пользователя')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email_address = models.EmailField(max_length=95, verbose_name='E-mail')
    allow_email_notification = models.BooleanField(default=False, verbose_name='E-mail уведомления')
    last_online = models.DateTimeField(auto_now=True, verbose_name='Последний онлайн')
    is_online = models.BooleanField(default=False, verbose_name='Онлайн')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    profile_picture = models.ImageField(upload_to='photos/%Y/%m/%d/', default='photos/default/default.png',
                                        verbose_name='Изображение профиля')
    user_role = models.ForeignKey('UserRole', models.PROTECT, default=get_default_user_role, verbose_name='Роль')
    enabled = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return '{} {}'.format(self.username, self.email_address)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_created']


def get_default_issue_status():
    """ get a default value for issue_status """
    return IssueStatus.objects.get(issue_status='OPEN')


class Issue(models.Model):
    project = models.ForeignKey('Project', models.CASCADE, verbose_name='Проект')
    reporter = models.ForeignKey(UserProfile, models.SET_NULL, null=True, verbose_name='Репортер')
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    time_estimate = models.DurationField(null=True, verbose_name='Оценка времени')
    due_date = models.DateTimeField(verbose_name='Выполнить до')
    date_submitted = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')  # надо исправить пустое значение
    last_change = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')
    issue_type = models.ForeignKey('IssueType', models.SET_NULL, null=True, verbose_name='Тип проблемы')
    issue_priority = models.ForeignKey('IssuePriority', models.SET_NULL, null=True, verbose_name='Приоритет проблемы')
    issue_status = models.ForeignKey('IssueStatus', models.SET_NULL, default=get_default_issue_status,
                                     null=True, verbose_name='Статус проблемы')
    issue_severity = models.ForeignKey('IssueSeverity', models.SET_NULL, null=True, verbose_name='Серьезность проблемы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'
        ordering = ['-added_date']


class IssueAssignee(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, verbose_name='Проблема')

    def __str__(self):
        return '{} assignee to {}'.format(self.user, self.issue)

    class Meta:
        verbose_name = 'Правоприемник проблемы'
        verbose_name_plural = 'Правоприемники проблемы'
        ordering = ['-id']


class IssueNote(models.Model):
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    note_text = models.TextField(verbose_name='Текст')
    note_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    user = models.ForeignKey(UserProfile, models.SET_NULL, null=True, verbose_name='Пользователь')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, verbose_name='Проблема')

    def __str__(self):
        return '{} wrote {} to {}'.format(self.user, self.title, self.issue)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-note_date']


class Project(models.Model):
    project_name = models.CharField(max_length=120, verbose_name='Проект')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-id']


class ProjectAccess(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    access_type = models.ForeignKey('AccessType', on_delete=models.CASCADE, verbose_name='Тип доступа')

    def __str__(self):
        return '{} {} {}'.format(self.project, self.user, self.access_type)

    class Meta:
        verbose_name = 'Доступ к проекту'
        verbose_name_plural = 'Доступ к проектам'
        ordering = ['-id']


class UserRole(models.Model):
    ADMIN = 'ADMINISTRATOR'  # can do everything
    MODER = 'MODERATOR'      # like admin but less
    USER = 'USER'            # authorized user

    USER_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODER, 'Модератор'),
        (USER, 'Пользователь'),
    )

    user_role = models.CharField(max_length=15,
                                 choices=USER_CHOICES,
                                 default=USER,
                                 verbose_name='Роль')

    def __str__(self):
        return self.user_role

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        ordering = ['id']


class IssueSeverity(models.Model):
    BLOCK = 'BLOCKER'  # cause of product failure
    CRIT = 'CRITICAL'  # cause of partial product failure
    MAJOR = 'MAJOR'    # some of the main logic works incorrectly
    MINOR = 'MINOR'    # doesn't break logic
    TRIV = 'TRIVIAL'   # doesn't affect the overall quality of product

    SEVERITY_CHOICES = (
        (BLOCK, 'Блокатор'),
        (CRIT, 'Критичная'),
        (MAJOR, 'Крупная'),
        (MINOR, 'Незначительная'),
        (TRIV, 'Тривиальная'),
    )

    issue_severity = models.CharField(max_length=9,
                                      choices=SEVERITY_CHOICES,
                                      null=True,
                                      default=TRIV,
                                      verbose_name='Серьезность')

    def __str__(self):
        return self.issue_severity

    class Meta:
        verbose_name = 'Серьезность проблемы'
        verbose_name_plural = 'Серьезность проблем'
        ordering = ['id']


class IssuePriority(models.Model):
    HIGHEST = 'HIGHEST'  # will block progress
    HIGH = 'HIGH'        # could block progress
    MEDIUM = 'MEDIUM'    # potential to affect progress
    LOW = 'LOW'          # easily worked around
    LOWEST = 'LOWEST'    # little or no impact on progress

    PRIORITY_CHOICES = (
        (HIGHEST, 'Самый высокий'),
        (HIGH, 'Высокий'),
        (MEDIUM, 'Средний'),
        (LOW, 'Низкий'),
        (LOWEST, 'Самый низкий'),
    )

    issue_rank = models.CharField(max_length=8,
                                  choices=PRIORITY_CHOICES,
                                  default=MEDIUM,
                                  verbose_name='Ранк')

    def __str__(self):
        return self.issue_rank

    class Meta:
        verbose_name = 'Приоритет проблемы'
        verbose_name_plural = 'Приоритеты проблем'
        ordering = ['id']


class IssueType(models.Model):
    BUG = 'BUG'              # impairs or prevents the functions of a product
    EPIC = 'EPIC'            # group bugs and tasks, needs to be broken down
    IMPROVE = 'IMPROVEMENT'  # improvement of product functions
    FEATURE = 'FEATURE'      # new capability or feature
    TASK = 'TASK'            # work that needs to be done
    SUBTASK = 'SUBTASK'      # work that is required to complete a task

    TYPE_CHOICES = (
        (BUG, 'Баг'),
        (EPIC, 'Эпик'),
        (IMPROVE, 'Улучшение'),
        (FEATURE, 'Новый функционал'),
        (TASK, 'Задача'),
        (SUBTASK, 'Подзадача'),
    )

    issue_type = models.CharField(max_length=12,
                                  choices=TYPE_CHOICES,
                                  default=TASK,
                                  verbose_name='Тип')

    def __str__(self):
        return self.issue_type

    class Meta:
        verbose_name = 'Тип проблемы'
        verbose_name_plural = 'Типы проблем'
        ordering = ['id']


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
        (OPEN, 'Открыта'),
        (PROGRESS, 'В процессе'),
        (DONE, 'Сделано'),
        (TODO, 'Сделать'),
        (REVIEW, 'В рассмотрении'),
        (APPROVED, 'Принято'),
        (REJECTED, 'Отклонено'),
        (CANCELLED, 'Отменено'),
    )

    issue_status = models.CharField(max_length=10,
                                    choices=STATUS_CHOICES,
                                    default=OPEN,
                                    verbose_name='Статус')

    def __str__(self):
        return self.issue_status

    class Meta:
        verbose_name = 'Статус проблемы'
        verbose_name_plural = 'Статусы проблем'
        ordering = ['id']


class AccessType(models.Model):
    GUEST = 'GUEST'          # random person not from the project
    DEV = 'DEVELOPER'        # developer of the project
    MAINTAIN = 'MAINTAINER'  # maintain the project
    OWNER = 'OWNER'          # own the project

    ACCESS_TYPE = (
        (GUEST, 'Гость'),
        (DEV, 'Разработчик'),
        (MAINTAIN, 'Сопроводитель'),
        (OWNER, 'Владелец'),
    )

    access_type = models.CharField(max_length=11,
                                   choices=ACCESS_TYPE,
                                   default=GUEST,
                                   verbose_name='Тип доступа')

    def __str__(self):
        return self.access_type

    class Meta:
        verbose_name = 'Тип доступа к проекту'
        verbose_name_plural = 'Типы доступа к проекту'
        ordering = ['id']


# class RelatedIssue(models.Model):
#     source_issue = models.ForeignKey(Issue, related_name=, on_delete=models.CASCADE)
#     destination_issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{} to {}'.format(self.source_issue, self.destination_issue)
