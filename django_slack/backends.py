import pprint
import logging

from six.moves import urllib

from django.http.request import QueryDict
from django.utils.module_loading import import_string

from .utils import Backend
from .app_settings import app_settings

logger = logging.getLogger(__name__)

class UrllibBackend(Backend):
    def send(self, url, data, **kwargs):
        qs = QueryDict(mutable=True)
        qs.update(data)

        r = urllib.request.urlopen(urllib.request.Request(
            url,
            qs.urlencode().encode('utf-8'),
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

Urllib2Backend = UrllibBackend # For backwards-compatibility
