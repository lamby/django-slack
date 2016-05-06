import json

from django.conf import settings
from django.template.loader import render_to_string

from .utils import get_backend
from .app_settings import app_settings

def slack_message(template, context=None, attachments=None, fail_silently=None, **kwargs):
    backend = get_backend()
    data = {}
    context = dict(context or {}, settings=settings)
    if fail_silently is None:
        fail_silently = app_settings.FAIL_SILENTLY

    for k, v in {
        'text': {
            'default': '',
            'required': False, # Checked later
        },
        'token': {
            'default': app_settings.TOKEN,
            'required': True,
        },
        'channel': {
            'default': app_settings.CHANNEL,
            'required': False, # Checked later
        },
        'icon_url': {
            'default': app_settings.ICON_URL,
            'required': False,
        },
        'icon_emoji': {
            'default': app_settings.ICON_EMOJI,
            'required': False,
        },
        'username': {
            'default': app_settings.USERNAME,
            'required': False,
        },
        'attachments': {
            'default': attachments,
            'render': False,
            'required': False,
        },
        'endpoint_url': {
            'default': app_settings.ENDPOINT_URL,
            'render': True,
            'required': False,
        },
    }.items():
        # First, set from default if we have one
        if v['default']:
            data[k] = v['default']

        # Render template if necessary
        if v.get('render', True):
            try:
                val = render_to_string(template, dict(
                    context,
                    django_slack='django_slack/%s' % k,
                )).strip().encode('utf8', 'ignore')
            except Exception:
                if fail_silently:
                    return
                raise

            if val:
                data[k] = val

        # Check if paramater is required
        if v['required']:
            if data.get(k, None):
                continue

            if fail_silently:
                return

            raise ValueError("Missing or empty required parameter: %s" % k)

    if 'text' not in data and 'attachments' not in data:
        raise ValueError("text parameter is required if attachments is not set")

    # The endpoint URL is not part of the data payload but as we construct it
    # within `data` we must remove it.
    endpoint_url = data.pop('endpoint_url')

    # If a custom endpoint URL was specified then we need to wrap it, otherwise
    # we need to ensure attachments are encoded.
    if endpoint_url == app_settings.DEFAULT_ENDPOINT_URL:
        # As a special case, if a custom endpoint is not set (eg. for a
        # private channel), then the channel parameter is not required.
        if not data.get('channel'):
            if fail_silently:
                return

            raise ValueError("channel parameter is required if custom " \
                "endpoint URL is not specified")

        if 'attachments' in data:
            data['attachments'] = json.dumps(data['attachments'])
    else:
        data = {'payload': json.dumps(data)}

    try:
        backend.send(endpoint_url, data, **kwargs)
    except Exception:
        if not fail_silently:
            raise
