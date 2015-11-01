from django.conf import settings

DEFAULT_ENDPOINT_URL = 'https://slack.com/api/chat.postMessage'

def setting(suffix, default):
    return getattr(settings, 'SLACK_%s' % suffix, default)

TOKEN = setting('TOKEN', None)
CHANNEL = setting('CHANNEL', '#general')
USERNAME = setting('USERNAME', 'bot')
LINK_NAMES = setting('LINK_NAMES', '0')
ICON_URL = setting('ICON_URL', None)
ICON_EMOJI = setting('ICON_EMOJI', None)
ENDPOINT_URL = setting('ENDPOINT_URL', DEFAULT_ENDPOINT_URL)

BACKEND = setting('BACKEND', 'django_slack.backends.%s' %
    ('DisabledBackend' if settings.DEBUG else 'UrllibBackend'))
FAIL_SILENTLY = setting('FAIL_SILENTLY', False)
