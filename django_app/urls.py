from django.urls import path
from .views import (
    greetings,
    get_all_tasks,
    get_unique_task,
    create_task,
    get_tasks_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView # Добавлен импорт SubTaskDetailUpdateDeleteView
)

urlpatterns = [
    path('home-page/', greetings),
    path('tasks/', get_all_tasks, name='task-list'),
    path('tasks/<int:pk>/', get_unique_task, name='task-detail'),
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/statistics/', get_tasks_statistics, name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete')
]