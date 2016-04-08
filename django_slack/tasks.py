from celery import task

try:
    from django.utils.module_loading import import_string
except ImportError:
    # support for django 1.6
    from django.utils.module_loading import import_by_path as import_string

from .app_settings import app_settings

@task
def send(*args, **kwargs):
    import_string(app_settings.BACKEND_FOR_QUEUE)().send(*args, **kwargs)
