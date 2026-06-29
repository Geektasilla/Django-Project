from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_app.models import Task
from django.core.mail import send_mail

@receiver(pre_save, sender=Task)
def notify_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_task = Task.objects.get(pk=instance.pk)
    print(f"DEBUG: Сравниваю '{old_task.status}' и '{instance.status}'")

    if old_task.status != instance.status:
        print("DEBUG: Статусы разные! Отправляем письмо...")
        if instance.status == 'Done':
            send_mail(
                'Задача закрыта',
                f'Задача {instance.id} была закрыта.',
                'admin@gmail.com',
                [instance.owner.email]
            )
        else:
            send_mail(
                'Статус обновлен',
                f'Статус задачи {instance.id} изменен на {instance.status}.',
                'admin@gmail.com',
                [instance.owner.email]
            )