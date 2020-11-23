from celery import shared_task

from django.utils.module_loading import import_string

from .app_settings import app_settings


@shared_task
def send(*args, **kwargs):
    backend = import_string(app_settings.BACKEND_FOR_QUEUE)()

    return backend.send(*args, **kwargs)
