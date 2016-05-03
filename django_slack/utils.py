import json

from django.utils.module_loading import import_string

from .exceptions import LABEL_TO_EXCEPTION, SlackException
from .app_settings import app_settings

class Backend(object):
    def send(self, url, data):
        raise NotImplementedError()

    def validate(self, content_type, content):
        if content_type.startswith('application/json'):
            result = json.loads(content)

            if not result['ok']:
                klass = LABEL_TO_EXCEPTION.get(result['error'], SlackException)

                raise klass(result['error'])

        elif content != 'ok':
            raise SlackException(content)

def get_backend():
    """
    Wrap the backend in a function to not load it at import time.
    get_backend() caches the backend on first call.
    """
    if get_backend.backend is None:
        get_backend.backend = import_string(app_settings.BACKEND)()
    return get_backend.backend
get_backend.backend = None
