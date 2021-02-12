from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('projects/', projects_list, name='projects'),
    path('projects/<int:project_id>/', project_details, name='project_details'),
]