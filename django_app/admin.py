from django.contrib import admin
from django_app.models import Task, Category, SubTask

admin.site.register(Task)
admin.site.register(Category)
admin.site.register(SubTask)
