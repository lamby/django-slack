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

def get_backend(name=None):
    """
    Wrap the backend in a function to not load it at import time.
    get_backend() caches the backend on first call.

    :param name: optional string name for backend, otherwise take from settings
    :type name: str or unicode or None
    """
    loaded_backend = get_backend.backend
    # load the backend if we have a provided name, or if this function's backend hasn't yet been set
    if name or not loaded_backend:
        loaded_backend = import_string(name or app_settings.BACKEND)()
        # if the backend hasn't been cached yet, and we didn't get a custom name passed in, cache the backend
        if not (get_backend.backend or name):
            get_backend.backend = loaded_backend
    return loaded_backend
get_backend.backend = None
