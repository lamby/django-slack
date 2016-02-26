from django.conf import settings


class AppSettings(object):
    def _get_setting(suffix, default):
        def setting(self):
            return getattr(settings, 'SLACK_%s' % suffix, default)

        return setting

    TOKEN = property(_get_setting('TOKEN', None))
    CHANNEL = property(_get_setting('CHANNEL', '#general'))
    USERNAME = property(_get_setting('USERNAME', 'bot'))
    ICON_URL = property(_get_setting('ICON_URL', None))
    ICON_EMOJI = property(_get_setting('ICON_EMOJI', None))

    DEFAULT_ENDPOINT_URL = 'https://slack.com/api/chat.postMessage'
    ENDPOINT_URL = property(_get_setting('ENDPOINT_URL', DEFAULT_ENDPOINT_URL))

    _DEFAULT_BACKEND = 'django_slack.backends.DisabledBackend' if settings.DEBUG else \
        'django_slack.backends.UrllibBackend'
    BACKEND = property(_get_setting('BACKEND', _DEFAULT_BACKEND))
    BACKEND_FOR_QUEUE = property(_get_setting('BACKEND_FOR_QUEUE', _DEFAULT_BACKEND))

    FAIL_SILENTLY = property(_get_setting('FAIL_SILENTLY', False))

app_settings = AppSettings()
