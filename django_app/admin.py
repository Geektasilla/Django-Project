from django.contrib import admin
from django_app.models import Task, Category, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'status',
        'deadline',
        'created_at'
    )
    search_fields = (
        'title',
        'description'

    )
    list_filter = (
        'status',
        'created_at'
    )
    list_editable = (
        'status',
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'status',
        'task',
        'deadline',
        'created_at'
    )
    search_fields = (
        'title',
        'created_at'
    )
    list_filter = (
        'status',
        'created_at'
    )
    list_editable = (
        'status',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )





