from django.conf import settings
from django.test import TestCase, override_settings

from django_slack import slack_message
from django_slack.utils import get_backend
from django_slack.app_settings import app_settings

from tests.backends import RaisingBackend


class TestOverride(TestCase):
    def setUp(self):
        # Fake the backend not having been initialized yet.
        get_backend.backend = None

    def test_override(self):
        """
        Ensure that accessing a setting in an override works.
        """
        DISABLED_BACKEND = 'django_slack.backends.DisabledBackend'
        with override_settings(SLACK_BACKEND=DISABLED_BACKEND):
            self.assertEqual(settings.SLACK_BACKEND, DISABLED_BACKEND)
            self.assertEqual(app_settings.BACKEND, DISABLED_BACKEND)

    def test_backend_cache(self):
        """
        Ensure that the backend is cached once it is called once.
        """
        self.assertEqual(id(get_backend()), id(get_backend()))

    def test_backend_override(self):
        """
        Ensure the backend can be overridden.
        """
        with override_settings(SLACK_BACKEND='tests.backends.RaisingBackend'):
            with self.assertRaises(RaisingBackend.RaisedException):
                slack_message('test.slack', {'text': 'test'})

    def test_fail_silently(self):
        """
        Ensure fail silently can be overridden.
        """
        # Note that this will fail if test_backend_override ever fails.
        with override_settings(
            SLACK_FAIL_SILENTLY=True,
            SLACK_BACKEND='tests.backends.RaisingBackend',
        ):
            slack_message('test.slack', {'text': 'test'})
