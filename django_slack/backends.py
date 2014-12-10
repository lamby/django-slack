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

class ConsoleBackend(Backend):
    def send(self, url, data, fail_silently):
        print "I: Slack message:"
        pprint.pprint(data, indent=4)
        print "-" * 79

class DisabledBackend(Backend):
    def send(self, url, data, fail_silently):
        pass
