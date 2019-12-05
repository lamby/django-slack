from django.conf import settings


def setting(suffix, default):
    @property
    def fn(self):
        return getattr(settings, 'SLACK_{}'.format(suffix), default)

    return fn


class AppSettings(object):
    DEFAULT_ENDPOINT_URL = 'https://slack.com/api/chat.postMessage'
    DEFAULT_BACKEND = (
        'django_slack.backends.DisabledBackend'
        if settings.DEBUG
        else 'django_slack.backends.UrllibBackend'
    )

    TOKEN = setting('TOKEN', None)
    CHANNEL = setting('CHANNEL', '#general')
    USERNAME = setting('USERNAME', 'bot')
    ICON_URL = setting('ICON_URL', None)
    ICON_EMOJI = setting('ICON_EMOJI', None)

    ENDPOINT_URL = setting('ENDPOINT_URL', DEFAULT_ENDPOINT_URL)

    BACKEND = setting('BACKEND', DEFAULT_BACKEND)
    BACKEND_FOR_QUEUE = setting('BACKEND_FOR_QUEUE', DEFAULT_BACKEND)

    FAIL_SILENTLY = setting('FAIL_SILENTLY', False)
    AS_USER = setting('AS_USER', False)


app_settings = AppSettings()
