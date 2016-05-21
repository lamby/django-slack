import pprint
import logging

from six.moves import urllib

from django.utils.module_loading import import_string

from .utils import Backend
from .app_settings import app_settings

logger = logging.getLogger(__name__)

class UrllibBackend(Backend):
    def send(self, url, data, **kwargs):
        r = urllib.request.urlopen(urllib.request.Request(
            url,
            # make sure
            urllib.parse.urlencode(data).encode('utf-8'),
        ))

        result = r.read().decode('utf-8')

        self.validate(r.headers['content-type'], result)

class RequestsBackend(Backend):
    def __init__(self):
        # Lazily import to avoid dependency
        import requests

        self.session = requests.Session()

    def send(self, url, data, **kwargs):
        r = self.session.post(url, data=data, verify=False)

        self.validate(r.headers['Content-Type'], r.text)

class ConsoleBackend(Backend):
    def send(self, url, data, **kwargs):
        print("I: Slack message:")
        pprint.pprint(data, indent=4)
        print("-" * 79)

class LoggerBackend(Backend):
    def send(self, url, data, **kwargs):
        logger.info(pprint.pformat(data, indent=4))

class DisabledBackend(Backend):
    def send(self, url, data, **kwargs):
        pass


class _AsyncBackend(Backend):
    def __init__(self):
        self._send = self.init_sender()

        # Check we can import our specified backend up-front
        import_string(app_settings.BACKEND_FOR_QUEUE)()

    def send(self, *args, **kwargs):
        # Send asynchronously via Celery
        self._send.delay(*args, **kwargs)

    def init_sender(self):
        # Lazily import to avoid dependency
        # subclass this must implement this method
        raise NotImplementedError()


class CeleryBackend(_AsyncBackend):

    def init_sender(self):
        from .celery_task import celery_task
        return celery_task


class RQBackend(_AsyncBackend):

    def init_sender(self):
        from .tasks import get_rq_task
        return get_rq_task()


Urllib2Backend = UrllibBackend # For backwards-compatibility
