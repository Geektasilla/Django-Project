from rest_framework import serializers
from .models import Task, SubTask, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at']
