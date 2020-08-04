import pprint
import logging
import urllib.request

from django.http.request import QueryDict
from django.utils.module_loading import import_string

from .utils import Backend
from .app_settings import app_settings

logger = logging.getLogger(__name__)


class UrllibBackend(Backend):
    def send(self, url, message_data, **kwargs):
        qs = QueryDict(mutable=True)
        qs.update(message_data)

        r = urllib.request.urlopen(
            urllib.request.Request(url, qs.urlencode().encode('utf-8'),)
        )

        result = r.read().decode('utf-8')

        return self.validate(r.headers['content-type'], result, message_data)


class RequestsBackend(Backend):
    def __init__(self):
        # Lazily import to avoid dependency
        import requests

        self.session = requests.Session()

    def send(self, url, message_data, **kwargs):
        r = self.session.post(url, data=message_data)

        return self.validate(r.headers['Content-Type'], r.text, message_data)


class ConsoleBackend(Backend):
    def send(self, url, message_data, **kwargs):
        print("I: Slack message:")
        pprint.pprint(message_data, indent=4)
        print("-" * 79)


class LoggerBackend(Backend):
    def send(self, url, message_data, **kwargs):
        logger.info(pprint.pformat(message_data, indent=4))


class DisabledBackend(Backend):
    def send(self, url, message_data, **kwargs):
        pass


class CeleryBackend(Backend):
    def __init__(self):
        # Lazily import to avoid dependency
        from .tasks import send

        self._send = send

        # Check we can import our specified backend up-front
        import_string(app_settings.BACKEND_FOR_QUEUE)()

    def send(self, *args, **kwargs):
        # Send asynchronously via Celery
        self._send.delay(*args, **kwargs)


class DjangoQBackend(Backend):
    def __init__(self):
        # Check we can import our specified backend up-front
        import_string(app_settings.BACKEND_FOR_QUEUE)()

    @staticmethod
    def _send(*args, **kwargs):
        backend = import_string(app_settings.BACKEND_FOR_QUEUE)()
        return backend.send(*args, **kwargs)

    def send(self, *args, **kwargs):
        # Send asynchronously via Django-Q
        from django_q.tasks import async_task

        async_task(self._send, *args, group='django-slack', q_options=kwargs)


class TestBackend(Backend):
    """
    This backend is for testing.

    Before a test, call `reset_messages`, and after a test, call
    `retrieve_messages` for a list of all messages that have been sent during
    the test.
    """

    def __init__(self, *args, **kwargs):
        super(TestBackend, self).__init__(*args, **kwargs)
        self.reset_messages()

    def send(self, url, message_data, **kwargs):
        self.messages.append(message_data)

    def reset_messages(self):
        self.messages = []

    def retrieve_messages(self):
        messages = self.messages
        self.reset_messages()
        return messages


# For backwards-compatibility
Urllib2Backend = UrllibBackend
