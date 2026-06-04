from django.utils import timezone # Corrected import for timezone

from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer

def greetings(request: HttpRequest) -> HttpResponse:
  return HttpResponse('HELLO FROM OUR FIRST VIEW!!!')


@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_unique_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_tasks_statistics(request):
  total_tasks = Task.objects.count()
  tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))
  overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

  data = {
    'total_tasks': total_tasks,
    'tasks_by_status': tasks_by_status,
    'overdue_tasks': overdue_tasks
  }

  return Response(data)


class SubTaskListCreateView(APIView):
    """
    Представление для получения списка всех подзадач и создания новой подзадачи.
    """
    def get(self, request, format=None):
        """
        Обрабатывает GET-запросы для получения списка всех подзадач.
        """
        subtasks = SubTask.objects.all() # Получаем все объекты SubTask
        serializer = SubTaskCreateSerializer(subtasks, many=True) # Сериализуем их, указывая many=True для списка
        return Response(serializer.data) # Возвращаем сериализованные данные

    def post(self, request, format=None):
        """
        Обрабатывает POST-запросы для создания новой подзадачи.
        """
        serializer = SubTaskCreateSerializer(data=request.data) # Создаем экземпляр сериализатора с данными из запроса
        if serializer.is_valid(): # Проверяем валидность данных
            serializer.save() # Если данные валидны, сохраняем новую подзадачу
            return Response(serializer.data, status=status.HTTP_201_CREATED) # Возвращаем созданный объект и статус 201 Created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Если данные невалидны, возвращаем ошибки и статус 400 Bad Request


class SubTaskDetailUpdateDeleteView(APIView):
    """
    Представление для получения, обновления и удаления одной подзадачи по её ID.
    """
    def get_object(self, pk):
        """
        Вспомогательный метод для получения объекта SubTask или вызова 404.
        """
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request, pk, format=None):
        """
        Обрабатывает GET-запросы для получения деталей одной подзадачи.
        """
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обрабатывает PUT-запросы для полного обновления подзадачи.
        """
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Обрабатывает PATCH-запросы для частичного обновления подзадачи.
        """
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Обрабатывает DELETE-запросы для удаления подзадачи.
        """
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
