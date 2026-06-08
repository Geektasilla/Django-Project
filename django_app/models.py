from django.db import models


STATUS_CHOICES = [
    ('New', 'New'),
    ('In_progress', 'In_progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done')
]


class Category(models.Model):
    """
    Category of execution.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)


class Task(models.Model):
    """
    Task for execution.
    """
    title = models.CharField(max_length=100, unique_for_date='created_at')
    description = models.TextField()
    categories = models.ManyToManyField('Category')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        db_table = 'task_manager_task'
        verbose_name = 'Task'
        unique_together = ('title',)
        ordering = ('-created_at',)



class SubTask(models.Model):
    """
    Part of the main task (Task).
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'SubTask'
        unique_together = ('title',)
        ordering = ('-created_at',)







