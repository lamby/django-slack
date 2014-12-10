import pprint
import urllib
import urllib2

from .utils import Backend

class UrllibBackend(Backend):
    def send(self, url, data, fail_silently):
        request = urllib2.Request(url, data=urllib.urlencode(data))

        try:
            urllib2.urlopen(request)
        except Exception:
            if not fail_silently:
                raise

class RequestsBackend(Backend):
    def __init__(self):
        # Lazily import requests to avoid dependency
        import requests

        self.session = requests.Session()

    def send(self, url, data, fail_silently):
        try:
            result = self.session.post(url, data=data, verify=False).json()

            if not result['ok']:
                raise ValueError(result['error'])
        except Exception:
            if not fail_silently:
                raise

class ConsoleBackend(Backend):
    def send(self, url, data, fail_silently):
        print "I: Slack message:"
        pprint.pprint(data, indent=4)
        print "-" * 79

class DisabledBackend(Backend):
    def send(self, url, data, fail_silently):
        pass
