from django.utils import timezone # Corrected import for timezone

from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

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






