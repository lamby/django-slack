from __future__ import print_function

import pprint
from six.moves import urllib
from .utils import Backend


class Urllib2Backend(Backend):
    def send(self, url, data):
        r = urllib.urlopen(urllib.Request(url, data=urllib.urlencode(data)))

        self.validate(r.headers['content-type'], r.read())


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
