import pprint

from six.moves import urllib

from .utils import Backend

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

Urllib2Backend = UrllibBackend # For backwards-compatibility
