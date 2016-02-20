from django import template
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import allow_lazy
from django.utils.safestring import SafeText, mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

_slack_escapes = {
    ord('&'): u'&amp;',
    ord('<'): u'&lt;',
    ord('>'): u'&gt;',
}

@register.filter(is_safe=True)
@stringfilter
def escapeslack(value):
    """
    Returns the given text with ampersands and angle brackets encoded for use in
    the Slack API, per the Slack API documentation:
    <https://api.slack.com/docs/formatting#how_to_escape_characters>

    This is based on django.template.defaultfilters.escapejs.
    """
    return mark_safe(force_text(value).translate(_slack_escapes))
escapeslack = allow_lazy(escapeslack, six.text_type, SafeText)
