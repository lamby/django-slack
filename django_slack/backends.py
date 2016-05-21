import pprint
import logging

from six.moves import urllib

from django.http.request import QueryDict

from .utils import Backend

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

    def send(self, url, data, **kwargs):
        from .celery_task import celery_task
        return celery_task.delay(url, data, **kwargs)


class RQBackend(Backend):

    def send(self, url, data, **kwargs):
        from .tasks import get_rq_task
        return get_rq_task().delay(url, data, **kwargs)


Urllib2Backend = UrllibBackend # For backwards-compatibility
