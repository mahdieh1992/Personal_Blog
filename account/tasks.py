from celery import shared_task
from time import sleep
from mail_templated import EmailMessage
from django_celery_results.models import TaskResult


@shared_task()
def send_email_register(template_name=None, context={}, *args, **kwargs):
    email = EmailMessage(template_name, context, *args, **kwargs)
    sleep(2)
    email.send()


@shared_task()
def delete_task_done():
    TaskResult.objects.filter(status="SUCCESS").delete()
