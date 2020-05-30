import json

from django.conf import settings
from django.utils.encoding import force_str
from django.template.loader import render_to_string

from .utils import get_backend
from .app_settings import app_settings


def slack_message(
    template,
    context=None,
    attachments=None,
    blocks=None,
    fail_silently=None,
    **kwargs,
):
    data = {}

    channel = kwargs.pop('channel', app_settings.CHANNEL)
    backend = get_backend(name=kwargs.pop('backend', None))

    context = dict(context or {}, settings=settings)
    if fail_silently is None:
        fail_silently = app_settings.FAIL_SILENTLY

    NOT_REQUIRED, DEFAULT_ENDPOINT, ALWAYS = range(3)

    PARAMS = {
        'text': {'default': '', 'required': NOT_REQUIRED,},  # Checked later
        'token': {
            'default': app_settings.TOKEN,
            'required': DEFAULT_ENDPOINT,
        },
        'channel': {'default': channel, 'required': DEFAULT_ENDPOINT,},
        'icon_url': {
            'default': app_settings.ICON_URL,
            'required': NOT_REQUIRED,
        },
        'icon_emoji': {
            'default': app_settings.ICON_EMOJI,
            'required': NOT_REQUIRED,
        },
        'username': {
            'default': app_settings.USERNAME,
            'required': NOT_REQUIRED,
        },
        'attachments': {
            'default': attachments,
            'render': False,
            'required': NOT_REQUIRED,
        },
        'blocks': {
            'default': blocks,
            'render': False,
            'required': NOT_REQUIRED,
        },
        'endpoint_url': {
            'default': app_settings.ENDPOINT_URL,
            'render': ALWAYS,
            'required': NOT_REQUIRED,
        },
        'as_user': {
            'default': app_settings.AS_USER,
            'render': False,
            'required': NOT_REQUIRED,
        },
    }

    for k, v in PARAMS.items():
        # First, set from default if we have one
        if v['default']:
            data[k] = v['default']

        # Render template if necessary
        if v.get('render', True):
            try:
                val = force_str(
                    render_to_string(
                        template,
                        dict(
                            context, django_slack='django_slack/{}'.format(k),
                        ),
                    ).strip()
                )
            except Exception:
                if fail_silently:
                    return
                raise

            if val:
                data[k] = val

        # Check if paramater is required
        if v['required'] == ALWAYS:
            if data.get(k, None):
                continue

            if fail_silently:
                return

            raise ValueError(
                "Missing or empty required parameter: {}".format(k)
            )

    if 'text' not in data and 'attachments' not in data:
        raise ValueError(
            "text parameter is required if attachments is not set",
        )

    # Ensure that as_user is either "true" or not present (rather than "True"
    # or "False", etc.).
    #
    # This also prevents an encoding error under (just) Django 2.1 due to an
    # upstream regression (<https://github.com/lamby/django-slack/issues/85>).
    #
    if data.pop('as_user', app_settings.AS_USER):
        data['as_user'] = 'true'

    # The endpoint URL is not part of the data payload but as we construct it
    # within `data` we must remove it.
    endpoint_url = data.pop('endpoint_url')

    # If a custom endpoint URL was specified then we need to wrap it, otherwise
    # we need to ensure attachments are encoded.
    if endpoint_url == app_settings.DEFAULT_ENDPOINT_URL:
        # Check parameters that are only required if we don't specify a custom
        # endpoint URL.
        for k, v in PARAMS.items():
            if v['required'] != DEFAULT_ENDPOINT:
                continue

            if not data.get(k, None):
                if fail_silently:
                    return

                raise ValueError(
                    "{} parameter is required if custom endpoint URL is not "
                    "specified".format(k),
                )

        for x in ('attachments', 'blocks'):
            if x in data:
                data[x] = json.dumps(data[x])
    else:
        data = {'payload': json.dumps(data)}

    try:
        return backend.send(endpoint_url, data, **kwargs)
    except Exception:
        if not fail_silently:
            raise
