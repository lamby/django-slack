from django_slack.utils import Backend

class StorageBackend(Backend):
    """A backend which stores the messages sent."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Clear any messages."""
        self.messages = []

    def send(self, url, data):
        self.messages.append({
            'url': url,
            'data': data,
        })
