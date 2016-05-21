from __future__ import absolute_import

from .tasks import _sender

from celery import task

celery_task = task(_sender)
