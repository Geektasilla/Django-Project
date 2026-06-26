from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    greetings,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    SubTaskListCreateAPIView,
    SubTaskRetrieveUpdateDestroyAPIView,
    CategoryViewSet,
    UserRegistrationAPIView,
    LoginUser,
    LogoutUser
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('home-page/', greetings),
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view()),

    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

    path('', include(router.urls)),
]
