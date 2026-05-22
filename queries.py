import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_app.models import Task, SubTask


# task_deadline_date = timezone.now() + timedelta(days=3)
# main_task = Task.objects.create(
#     title="Prepare presentation",
#     description="Prepare materials and slides for the presentation",
#     status="New",
#     deadline=task_deadline_date
# )

# get_task = Task.objects.get(id=4)
# subtask_deadline_date = timezone.now() + timedelta(days=2)
# SubTask.objects.create(
#     title="Gather information",
#     description="Find necessary information for the presentation",
#     status="New",
#     deadline=subtask_deadline_date,
#     task=get_task
# )
#
# subtask_deadline_date = timezone.now() + timedelta(days=1)
# SubTask.objects.create(
#     title="Create slides",
#     description="Create presentation slides",
#     status="New",
#     deadline=subtask_deadline_date,
#     task=get_task
# )

# task_with_new_status = Task.objects.filter(status__iexact='new')
# print(f'Tasks with status "New":', ', '.join([task.title for task in task_with_new_status]))
#
# subtask_with_done_status = SubTask.objects.filter(status__iexact='done', deadline__lt=timezone.now())
# print(f'Tasks with status "Done":', ', '.join([subtask.title for subtask in subtask_with_done_status]))

#
# get_task = Task.objects.get(id=4)
# get_task.status = 'In progress'
# get_task.save()
#
# get_subtask = SubTask.objects.get(id=3)
# get_subtask.deadline = timezone.now() + timedelta(days=-2)
# get_subtask.save()
#
# get_subtask = SubTask.objects.get(id=2)
# get_subtask.description = 'Create and format presentation slides'
# get_subtask.save()

# get_task = Task.objects.get(id=4)
# get_task.delete()
# get_subtask = SubTask.objects.get(id=3)
# get_subtask.delete()



