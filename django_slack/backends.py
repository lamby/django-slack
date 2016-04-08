import pprint

from six.moves import urllib

try:
    from django.utils.module_loading import import_string
except ImportError:
    # support for django 1.6
    from django.utils.module_loading import import_by_path as import_string

from .utils import Backend
from .app_settings import app_settings

class UrllibBackend(Backend):
    def send(self, url, data):
        r = urllib.request.urlopen(urllib.request.Request(
            url,
            urllib.parse.urlencode(data).encode('utf-8'),
        ))

        result = r.read().decode('utf-8')

        self.validate(r.headers['content-type'], result)

class RequestsBackend(Backend):
    def __init__(self):
        # Lazily import to avoid dependency
        import requests

        self.session = requests.Session()

    def send(self, url, data):
        r = self.session.post(url, data=data, verify=False)

        self.validate(r.headers['Content-Type'], r.text)

class ConsoleBackend(Backend):
    def send(self, url, data):
        print("I: Slack message:")
        pprint.pprint(data, indent=4)
        print("-" * 79)

class DisabledBackend(Backend):
    def send(self, url, data):
        pass

class CeleryBackend(Backend):
    def __init__(self):
        # Lazily import to avoid dependency
        from .tasks import send
        self.send = send

        # Check we can import our specified backend up-front
        import_string(app_settings.BACKEND_FOR_QUEUE)()

    def send(self, *args, **kwargs):
        # Send asynchronously via Celery
        self.send.delay(*args, **kwargs)

Urllib2Backend = UrllibBackend # For backwards-compatibility
