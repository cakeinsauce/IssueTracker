from django.urls import path

from .views import *

urlpatterns = [
    path('users/', users),
    path('projects/', projects_list),
    path('projects/<int:project_id>/', project_details)
]