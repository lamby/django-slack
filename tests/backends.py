from django_slack.utils import Backend

class StorageBackend(Backend):
    """
    A backend that stores all messages sent.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Clear any messages.
        """
        self.messages = []

    def send(self, url, data):
        self.messages.append({
            'url': url,
            'data': data,
        })

class RaisingBackend(Backend):
    """
    A backend which raises when asked to send a message.
    """
    class RaisedException(Exception):
        pass

    def send(self, url, data):
        raise RaisingBackend.RaisedException(url, data)
