"""
============
django-slack
============

-------------------------------------
Seamless Slack integration for Django
-------------------------------------

This project provides easy-to-use integration between
`Django <http://www.djangoproject.com/>`_ projects and the
`Slack <https://www.slack.com>`_ group chat and IM tool.

* Uses the templating system, rather than constructing messages "by hand" in
  your ``views.py`` and ``models.py``.

* Easily enabled and disabled in certain environments, preventing DRY
  violations by centralising the logic to avoid sending messages in development
  or staging environments.

* Pluggable backend system for greater control over exactly how messages are
  transmitted to the Slack API (eg. sent asynchronously using your queuing
  system)

Installation
------------

#. Add ``django_slack`` to ``INSTALLED_APPS``.

#. Ensure ``django.template.loaders.app_directories.Loader`` is in your
   ``TEMPLATE_LOADERS``.

Usage
-----

To send a messsage::

    from django_slack import slack_message

    slack_message('path/to/my_message.slack', {
        'foo': Foo.objects.get(pk=17),
    })

Where ``path/to/my_message.slack`` (in your templates directory) might
contain::

    {% extends django_slack %}

    {% block text %}
    Message text here: {{ foo.bar|urlize }}
    {% endblock %}

    {% block channel %}
    #mychannel
    {% endblock %}

Required blocks:

* **text** -- contains the message you wish to send. HTML entities are automatically escaped.

Required blocks which can be defaulted globally and overridden (see *Configuration*):

* **channel** -- ID or name of the room.
* **username** -- Name the message will appear be sent from.
* **token** -- Your Slack authentication token (eg. ``xoxp-2398017930-3368047240-1193456476-96c313``)

Optional blocks:

* **icon_url** -- URL to an image to use as the icon for this message. (eg. `http://lorempixel.com/48/48`)
* **icon_emoji** -- Emoji to use as the icon for this message (eg. `:chart_with_upwards_trend:`). Overrides `icon_url`.

Richly-formatted messages
--------------------------

You can send any number of richly-formatted messages as attachments with a
given Slack message.

To send a message with an attachment.

#. Assemble your attachments as follows::

    attachments = [
        {
         'title': "Richly-formatted message title',
         'text': 'Richly-formatted message body.',
        },
    ]

#. Pass in your attachments to `slack_message` as an optional argument::

    from django_slack import slack_message

    slack_message('path/to/my_message.slack', {
        'foo': Foo.objects.get(pk=17),
    }, attachments)

You can assemble and send any number of message objects within the
`attachments` list. For more information on all available formatting options,
please visit the `Slack API Attachments Docs
<https://api.slack.com/docs/attachments>`_.

Configuration
-------------

``SLACK_TOKEN``
~~~~~~~~~~~~~~~

Default: ``None``

Your Slack authentication token. You can override on a per-message level by
specifying a ``{% block token %}{% endblock %}`` in your message templates.

You can generate a new token on this site: https://api.slack.com/web#authentication

``SLACK_CHANNEL``
~~~~~~~~~~~~~~~~~

Default: ``#general``

Use this setting to set a default channel of the room the message should appear
in.

You can override on a per-message level by specifying a
``{% block channel %}{% endblock %}`` in your message template.

``SLACK_USERNAME``
~~~~~~~~~~~~~~~~~~

Default: ``bot``

Use this setting to set a default name the message will appear be sent from.

You can override on a per-message level by specifying a
``{% block username %}{% endblock %}`` in your message template.

``SLACK_ICON_EMOJI``
~~~~~~~~~~~~~~~~~~~~

Default: ``None``

Use this setting to set a default icon emoji.

You can override on a per-message level by specifying a
``{% block icon_emoji %}{% endblock %}`` in your message template.

``SLACK_ICON_URL``
~~~~~~~~~~~~~~~~~~

Default: ``None``

Use this setting to set a default icon URL.

You can override on a per-message level by specifying a
``{% block icon_url %}{% endblock %}`` in your message template.

``SLACK_ENDPOINT_URL``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``https://slack.com/api/chat.postMessage'``

Use this setting to set a default endpoint URL. This is necessary to use
Slack's "Incoming Webhooks."

You can override on a per-message level by specifying a
``{% block endpoint_url %}{% endblock %}`` in your message template.

``SLACK_FAIL_SILENTLY``
~~~~~~~~~~~~~~~~~~~~~~~

Default: ``False``

Whether errors should be silenced or raised to the user. As Slack messages
are often for administrators of a site and not the users, masking temporary
errors with the Slack API may be desired.

``SLACK_BACKEND``
~~~~~~~~~~~~~~~~~

Default: ``"django_slack.backends.Urllib2Backend"`` (``"django_slack.backends.DisabledBackend"`` if ``settings.DEBUG``)

A string pointing to the eventual backend class that will actually send the
message to the Slack API. The default backend will send the message using the
Python ``urllib2`` library.

You can use this setting to globally disable sending messages to Slack. You
may need to set this to ``django_slack.backends.DisabledBackend`` when running
tests or in your staging environment if you do not already set ``DEBUG = True``
in these environments.

If you are using a queue processor, you can write a backend that wraps the
supplied ``Urllib2Backend`` backend so that messages are sent asynchronously and
do not delay processing of requests::

    from django_slack.utils import Backend
    from django_slack.backends import Urllib2Backend
    from django_lightweight_queue.task import task

    class QueuedBackend(Backend):
        def send(self, url, data, fail_silently):
            # Delegate to task
            send(url, data, fail_silently)

    # Must be directly importable.
    @task()
    def send(url, data, fail_silently):
        Urllib2Backend().send(url, data, fail_silently)

This would be enabled by setting ``SLACK_BACKEND`` to (for example)
``path.to.tasks.QueuedBackend``.

You can also use the supplied ``django_slack.backends.ConsoleBackend`` when
developing. Instead of actually sending the message to Slack, the console
backend just writes the emails that would be sent to standard output.

If you prefer to use Requests, please use
``django_slack.backends.RequestsBackend``.
"""

from .api import slack_message
