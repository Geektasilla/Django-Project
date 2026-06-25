from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from django_app.models import Task, SubTask, Category
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters, status
from django_app.serializers import TaskSerializer, SubTaskSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_app.pagination import CategoryPagination, MainCursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_app.permissions import IsOwner


class UserOwnedMixin:
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.queryset.none()

        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def greetings(request: HttpRequest) -> HttpResponse:
  return HttpResponse('HELLO FROM OUR FIRST VIEW!!!')


class TaskListCreateAPIView(UserOwnedMixin, ListCreateAPIView):
    """
    Представление для получения списка всех задач и создания новой задачи.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = MainCursorPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class TaskRetrieveUpdateDestroyAPIView(UserOwnedMixin, RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одной задачи по её ID.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = 'pk'


class SubTaskListCreateAPIView(UserOwnedMixin, ListCreateAPIView):
    """
    Представление для получения списка всех подзадач и создания новой задачи.
    """
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer
    pagination_class = MainCursorPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskRetrieveUpdateDestroyAPIView(UserOwnedMixin, RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одной подзадачи по её ID.
    """
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer
    lookup_field = 'pk'


class CategoryViewSet(ModelViewSet):
    """
    Представление для получения списка всех категорий и создания новой категории.
    """
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        tasks_count = self.queryset.annotate(
            task_count=Count('task')
        ).values(
            'name',
            'task_count'
        )
        return Response(tasks_count)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response ({"message": "Hello, authenticated user!", "user": request.user.username})


