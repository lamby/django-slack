import json

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
