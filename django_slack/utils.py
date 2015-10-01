import json

def from_dotted_path(fullpath):
    """
    Returns the specified attribute of a module, specified by a string.

    ``from_dotted_path('a.b.c.d')`` is roughly equivalent to::

        from a.b.c import d

    except that ``d`` is returned and not entered into the current namespace.
    """

    module, attr = fullpath.rsplit('.', 1)

    return getattr(__import__(module, {}, {}, (attr,)), attr)

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
