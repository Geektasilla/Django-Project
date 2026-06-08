from django.contrib import admin
from django_app.models import Task, Category, SubTask

class SubtaskInlineForm(admin.TabularInline):
    model = SubTask
    extra = 1
    max_num = 3

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubtaskInlineForm]
    list_display = (
        'short_title',
        'show_about',
        'status',
        'deadline',
        'created_at',
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

    def short_title(self, obj: Task)-> str:
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        else:
            return obj.title
    short_title.short_description = "title"

    @admin.display(description='About')
    def show_about(self, obj: Task)-> str:
        if not obj.description:
            return 'No descriptions'
        else:
            if len(obj.description) < 10:
                return obj.description
            else:
                return f"{obj.description[:50]}..."
    show_about.short_description = "about"


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

    @admin.action(description='Mark selected subtasks as Done')
    def  mark_subtasks_done(self, request, obj):
        obj.update(status='Done')
        
    actions = ['mark_subtasks_done']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )





