import mock

from django.test import TestCase, override_settings

from django_slack.utils import get_backend
from django_slack.backends import CeleryBackend, RQBackend


class TestCeleryBackends(TestCase):

    @classmethod
    def setUp(cls):
        get_backend.backend = None

    @mock.patch('django_slack.backends.CeleryBackend.send')
    def test_send(self, send):
        from django_slack.celery_task import celery_task
        from celery.registry import tasks
        BACKEND = 'django_slack.backends.CeleryBackend'
        with override_settings(SLACK_BACKEND=BACKEND):
            backend = get_backend()
            self.assertIsInstance(backend, CeleryBackend)

            # make sure we auto register the celery task
            self.assertEqual(tasks['django_slack.tasks._sender'], celery_task)
            self.assertTrue(hasattr(celery_task, 'delay'))
            self.assertTrue(hasattr(celery_task, 'apply_async'))


class TestRQBackends(TestCase):

    @classmethod
    def setUp(cls):
        get_backend.backend = None

    @mock.patch('django_slack.tasks.get_rq_task')
    @mock.patch('django_slack.backends.RQBackend.send')
    def test_send(self, send, get_rq_task):
        BACKEND = 'django_slack.backends.RQBackend'
        with override_settings(
                SLACK_RQ_QUEUE='default',
                SLACK_BACKEND=BACKEND):
            backend = get_backend()
            self.assertIsInstance(backend, RQBackend)

            worker = get_rq_task()
            # check if we got the right job instance
            self.assertTrue(hasattr(worker, 'delay'))

            backend.send()
            self.assertTrue(send.called)
