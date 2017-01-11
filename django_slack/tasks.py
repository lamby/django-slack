from django.utils.module_loading import import_string

from .app_settings import app_settings


def _sender(*args, **kwargs):
    return import_string(app_settings.BACKEND_FOR_QUEUE)().send(*args, **kwargs)


def get_rq_task(connection=None):
    from rq.decorators import job
    from django_rq.queues import get_queue
    return job(queue=get_queue(app_settings.BACKEND_QUEUE_NAME))(_sender)
