from django.http import HttpResponse, HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from django_app.models import Task, SubTask
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_app.serializers import TaskSerializer,  SubTaskSerializer


def greetings(request: HttpRequest) -> HttpResponse:
  return HttpResponse('HELLO FROM OUR FIRST VIEW!!!')


class TaskListCreateAPIView(ListCreateAPIView):
    """
    Представление для получения списка всех задач и создания новой задачи.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одной задачи по её ID.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
    allowed_methods = ['GET', 'PUT', 'PATCH', 'DELETE']



class SubTaskListCreateAPIView(ListCreateAPIView):
    """
    Представление для получения списка всех подзадач и создания новой задачи.
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одной подзадачи по её ID.
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'pk'
    allowed_methods = ['GET', 'PUT', 'PATCH', 'DELETE']