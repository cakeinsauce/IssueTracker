from django.shortcuts import render
from django.http import HttpResponse

from .models import UserProfile


def users(request):
    profiles = UserProfile.objects.all()
    context = {
        'profiles': profiles,
        'title': 'Список пользователей'
    }
    return render(request, 'tracker/users.html', context)
