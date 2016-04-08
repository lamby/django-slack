import json

try:
    from django.utils.module_loading import import_string
except ImportError:
    # support for django 1.6
    from django.utils.module_loading import import_by_path as import_string

from .app_settings import app_settings

class Backend(object):
    def send(self, url, data):
        raise NotImplementedError()

    def validate(self, content_type, content):
        if content_type.startswith('application/json'):
            result = json.loads(content)

            if not result['ok']:
                raise ValueError(result['error'])

        elif content != 'ok':
            raise ValueError(content)

def get_backend():
    """
    Wrap the backend in a function to not load it at import time.
    get_backend() caches the backend on first call.
    """
    if get_backend.backend is None:
        get_backend.backend = import_string(app_settings.BACKEND)()
    return get_backend.backend
get_backend.backend = None
