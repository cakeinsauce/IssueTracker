from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def projects_list(request):
    """getting all available projects to user"""
    projects = Project.objects.all()
    people = ProjectAccess.objects.exclude(access_type__access_type='GUEST')

    context = {
        'projects': projects,
        'people': people,
        'title': 'Проекты',
    }
    return render(request, 'tracker/projects.html', context)


def project_details(request, project_id):
    """getting detail information about the project"""
    project = Project.objects.get(pk=project_id)

    return render(request, 'tracker/project_details.html', {'project': project})


def users(request):
    profiles = UserProfile.objects.all()
    context = {
        'profiles': profiles,
        'title': 'Список пользователей'
    }
    return render(request, 'tracker/users.html', context)
