from django.urls import path
from .views import (
    greetings,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    SubTaskListCreateAPIView,
    SubTaskRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('home-page/', greetings),
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view())
]