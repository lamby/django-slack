from django.conf import settings

def setting(suffix, default):
    return getattr(settings, 'SLACK_%s' % suffix, default)

TOKEN = setting('TOKEN', None)
CHANNEL = setting('CHANNEL', '#general')
USERNAME = setting('USERNAME', 'bot')
ICON_URL = setting('ICON_URL', None)
ICON_EMOJI = setting('ICON_EMOJI', None)

BACKEND = setting('BACKEND', 'django_slack.backends.%s' %
    ('DisabledBackend' if settings.DEBUG else 'Urllib2Backend'))
FAIL_SILENTLY = setting('FAIL_SILENTLY', False)
