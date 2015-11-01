import pprint

from six.moves import urllib

from .utils import Backend


class UrllibBackend(Backend):
    def send(self, url, data):
        """
        Creates a POST request, sends it, captures the response and validates it.

        Note:
        The urllib.parse.urlencode() function takes a mapping
        or sequence of 2-tuples and returns a string in this format.
        It should be encoded to bytes before being used as the data parameter.
        """
        data = urllib.parse.urlencode(data)
        binary_data = data.encode('utf-8')
        request = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(request)
        result = response.readall().decode('utf-8')
        self.validate(response.headers['content-type'], result)


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


Urllib2Backend = UrllibBackend  # For backwards-compatibility
