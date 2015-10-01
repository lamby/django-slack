import json

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string

from . import app_settings
from .utils import from_dotted_path

backend = from_dotted_path(app_settings.BACKEND)()

def slack_message(template, context=None, attachments=None, fail_silently=app_settings.FAIL_SILENTLY):
    context = Context(context or {})

    context['settings'] = settings

    def render(component):
        component_template = 'django_slack/%s' % component

        return render_to_string(template, {
            'django_slack': component_template,
        }, context).strip().encode('utf8', 'ignore')

    data = {
        'text': '',
        'token': app_settings.TOKEN,
        'channel': app_settings.CHANNEL,
        'icon_url': app_settings.ICON_URL,
        'icon_emoji': app_settings.ICON_EMOJI,
        'username': app_settings.USERNAME,
        'endpoint_url': app_settings.ENDPOINT_URL,
    }

    # Filter actually defined values
    data = {k: v for k, v in data.iteritems() if v}

    # Render templates
    for part in ('token', 'channel', 'text', 'icon_url', 'icon_emoji', 'username', 'endpoint_url'):
        try:
            txt = render(part)
        except Exception:
            if fail_silently:
                return
            raise

        if txt:
            data[part] = txt

    # Check for required parameters
    for x in ('token', 'channel', 'text', 'endpoint_url'):
        if data.get(x, None):
            continue

        if fail_silently:
            return

        assert False, "Missing or empty required parameter: %s" % x

    if attachments is not None:
        data['attachments'] = json.dumps(attachments)

    # The endpoint URL is not part of the data payload but as we construct it
    # within `data` we must remove it.
    endpoint_url = data.pop('endpoint_url')

    # If a custom endpoint URL was specified then we need to wrap it
    if endpoint_url != app_settings.DEFAULT_ENDPOINT_URL:
        data = {'payload': json.dumps(data)}

    try:
        backend.send(endpoint_url, data)
    except Exception:
        if not fail_silently:
            raise
