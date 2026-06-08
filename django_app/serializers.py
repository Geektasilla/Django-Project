from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Task, SubTask, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']

class TaskCreateSerializer(serializers, ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Date cannot be in the past')
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at']

    def create(self, validate_data):
        name = validate_data.get('name')
        if name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError('Category with this name already exists')
        return Category.objects.create(**validate_data)

    def update(self, instance, validate_data):
        name = validate_data.get('name', instance.name)

        if name != instance.name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError('Category with this name already exists')

        return super().update(instance, validate_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    task = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']













