from django.urls import path
from .views import greetings, get_all_tasks, get_unique_task, create_task, get_tasks_statistics

urlpatterns = [
    path('home-page/', greetings),
    path('tasks/', get_all_tasks, name='task-list'),
    path('tasks/<int:pk>/', get_unique_task, name='task-detail'),
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/statistics/', get_tasks_statistics, name='task-statistics'),
]
