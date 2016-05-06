from celery import task

from django.utils.module_loading import import_string

from .app_settings import app_settings

@task
def send(*args, **kwargs):
    return import_string(app_settings.BACKEND_FOR_QUEUE)().send(*args, **kwargs)
