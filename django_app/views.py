from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django_app.models import Task, SubTask, Category
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters, status
from django_app.serializers import TaskSerializer, SubTaskSerializer, CategorySerializer, UserLoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils import timezone
from django_app.pagination import CategoryPagination, MainCursorPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_app.permissions import IsOwner
from django_app.utils import set_jwt_cookies, clear_cookies
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema

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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = 'pk'


class SubTaskListCreateAPIView(UserOwnedMixin, ListCreateAPIView):
    """
    Представление для получения списка всех подзадач и создания новой задачи.
    """
    queryset = SubTask.objects.all()
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer
    lookup_field = 'pk'


class CategoryViewSet(ModelViewSet):
    """
    Представление для получения списка всех категорий и создания новой категории.
    """
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response ({"message": "Hello, authenticated user!", "user": request.user.username})


class UserRegistrationAPIView(APIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        try:
            response = Response(
                {"message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED
            )
            set_jwt_cookies(response=response, user=user)
            return response

        except Exception as err:
            return Response(
                {"message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginUser(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request: Request, *args, **kwargs)-> Response:
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        try:
            refresh = RefreshToken.for_user(user)

            response = Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "Успешный вход",
                    "access": str(refresh.access_token)
                }
            )

            set_jwt_cookies(response=response, user=user)

            return response
        except Exception as err:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    "message": str(err)
                }
            )

class LogoutUser(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError:
                    pass
        except Exception as err:
            return Response(
                data={
                    "message": str(err)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(status=status.HTTP_200_OK)
        clear_cookies(response=response)

        return response