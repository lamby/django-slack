from django.conf import settings

class AppSettings(object):
    def get(suffix, default):
        def setting(self):
            return getattr(settings, 'SLACK_%s' % suffix, default)
        return setting

    TOKEN = property(get('TOKEN', None))
    CHANNEL = property(get('CHANNEL', '#general'))
    USERNAME = property(get('USERNAME', 'bot'))
    ICON_URL = property(get('ICON_URL', None))
    ICON_EMOJI = property(get('ICON_EMOJI', None))

    DEFAULT_ENDPOINT_URL = 'https://slack.com/api/chat.postMessage'
    ENDPOINT_URL = property(get('ENDPOINT_URL', DEFAULT_ENDPOINT_URL))

    _DEFAULT_BACKEND = 'django_slack.backends.DisabledBackend' if settings.DEBUG else \
        'django_slack.backends.UrllibBackend'
    BACKEND = property(get('BACKEND', _DEFAULT_BACKEND))
    BACKEND_FOR_QUEUE = property(get('BACKEND_FOR_QUEUE', _DEFAULT_BACKEND))

    FAIL_SILENTLY = property(get('FAIL_SILENTLY', False))

app_settings = AppSettings()
