from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django_app.choices import DAY_MAPPING
from django_app.models import Task, SubTask
from django_app.serializers import TaskSerializer, SubTaskCreateSerializer
from rest_framework.pagination import PageNumberPagination


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


@api_view(['GET'])
def get_tasks_by_day_of_week(request, day_name):
    day_name_lower = day_name.lower()
    day_number = DAY_MAPPING.get(day_name_lower)

    if day_number is None:
        return Response({"error": "Неверное название дня недели. Используйте полные названия дней, например 'monday'."}, status=status.HTTP_400_BAD_REQUEST)

    tasks = Task.objects.filter(deadline__week_day=day_number)
    serializer = TaskSerializer(tasks, many=True)
    return  Response(serializer.data)


class SubTaskPagination(PageNumberPagination):
    """
    Пагинация для подзадач.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


    # Этот метод get_page_number не нужен, так как page_size_query_param уже обрабатывает это.
    # так как для стандартного поведения PageNumberPagination он избыточен.
    # Но я оставила для наглядности, так как задания решала по порядку.
    # def get_page_number(self, request, page_size):
    #     page_size = request.query_params.get('page_size')
    #     if page_size and page_size.isdigit():
    #         return int(page_size)
    #     return self.page_size


class SubTaskListCreateView(APIView):
    """
    Представление для получения списка всех подзадач и создания новой подзадачи.
    """
    def get(self, request, format=None):
        """
        Обрабатывает GET-запросы для получения списка всех подзадач.
        """
        subtasks = SubTask.objects.all().order_by('-created_at')
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request, view=self)
        serializer = SubTaskCreateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request, format=None):
        """
        Обрабатывает POST-запросы для создания новой подзадачи.
        """
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    """
    Представление для получения, обновления и удаления одной подзадачи по её ID.
    """
    def subtask_instance(self, pk):
        """
        Вспомогательный метод для получения объекта SubTask или вызова 404.
        """
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request, pk, format=None):
        """
        Обрабатывает GET-запросы для получения деталей одной подзадачи.
        """
        subtask = self.subtask_instance(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обрабатывает PUT-запросы для полного обновления подзадачи.
        """
        subtask = self.subtask_instance(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Обрабатывает PATCH-запросы для частичного обновления подзадачи.
        """
        subtask = self.subtask_instance(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Обрабатывает DELETE-запросы для удаления подзадачи.
        """
        subtask = self.subtask_instance(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_filtered_subtasks(request):
    queryset = SubTask.objects.all().order_by('-created_at')

    task_title = request.query_params.get('task_title')
    subtask_status = request.query_params.get('status')

    if task_title:
        queryset = queryset.filter(task__title__icontains=task_title)
    
    if subtask_status:
        queryset = queryset.filter(status__iexact=subtask_status)

    paginator = SubTaskPagination()
    page = paginator.paginate_queryset(queryset, request, view=None)

    if page is None:
        serializer = SubTaskCreateSerializer(queryset, many=True)
        return Response(serializer.data)
    
    serializer = SubTaskCreateSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
