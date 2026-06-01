from rest_framework import serializers
from .models import Task # Corrected to relative import

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at'] # Added created_at back
        read_only_fields = ['created_at'] # Added read_only_fields back