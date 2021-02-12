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
    project_owner = ProjectAccess.objects.filter(access_type__access_type='OWNER').get(project=project_id)

    return render(request, 'tracker/project_details.html', {'project': project, 'project_owner': project_owner})


def index(request):
    profiles = UserProfile.objects.all()
    context = {
        'profiles': profiles,
        'title': 'Список пользователей'
    }
    return render(request, 'tracker/index.html', context)
