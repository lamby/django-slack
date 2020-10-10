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

#. Install via PyPI: ``pip install django-slack``.

#. Add ``django_slack`` to ``INSTALLED_APPS``.

#. Ensure `APP_DIRS` is enabled in your `TEMPLATES` settting.

#. Generate a token and store it in ``settings.SLACK_TOKEN``. See the next
   section for more information.

Tokens
------

For developing or testing, you should use a test token, which you can generate
at https://api.slack.com/docs/oauth-test-tokens

For production, you should use a bot's API token. Go to
https://my.slack.com/apps/A0F7YS25R-bots to view your bots. If you already have
a bot that you want to use with django-slack, click on its "Edit configuration"
button and copy its token from the "API Token" field. Otherwise, go to
https://my.slack.com/apps/new/A0F7YS25R-bots to create a new bot.

Usage
-----

To send a messsage::

    from django_slack import slack_message

    slack_message('path/to/my_message.slack', {
        'foo': Foo.objects.get(pk=17),
    })

Where ``path/to/my_message.slack`` (in your templates directory) might
contain:

.. code-block:: jinja

    {% extends django_slack %}

    {% block text %}
    Message text here: {{ foo.bar|urlize }} {{ foo.user.get_full_name|safe }}
    {% endblock %}

Required blocks:

* **text** -- contains the message you wish to send. HTML entities are
  automatically escaped. (See the
  `Slack documentation <https://api.slack.com/docs/formatting>`_ for more
  information.) If you wish to escape only the characters that MUST be escaped,
  you can use the ``escapeslack`` tag, which is automatically available:

  .. code-block:: jinja

    {% extends django_slack %}

    {% load django_slack %}

    {% block text %}
    This message will escape only the necessary characters for slack:
    {{ user.get_username|escapeslack }}
    {% endblock %}

  See the `Slack API message formatting documentation
  <https://api.slack.com/docs/message-formatting>`_ for more information on
  linking to users, URLs, etc.

Required blocks which can be defaulted globally and overridden (see
*Configuration*):

* **channel** -- ID or name of the room.
* **username** -- Name the message will appear be sent from.
* **token** -- Your Slack authentication token (eg.
  ``xoxp-2398017930-3368047240-1193456476-96c313``)

Optional blocks:

* **icon_url** -- URL to an image to use as the icon for this message. (eg.
  `http://lorempixel.com/48/48`)
* **icon_emoji** -- Emoji to use as the icon for this message (eg.
  `:chart_with_upwards_trend:`). Overrides `icon_url`.

Richly-formatted messages
--------------------------

You can send any number of richly-formatted messages as attachments with a
given Slack message.

To send a message with an attachment.

#. Assemble your attachments as follows::

    attachments = [
        {
         'title': 'Richly-formatted message title',
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

Rich message layouts
--------------------

You can send rich message layouts by using **layout blocks** and **block elements**.

To send a message with a block.

#. Define your blocks::

    blocks = [
        {
         'type': 'divider',
        }
    ]

#. Pass in your blocks to `slack_message` as an optional argument::

    from django_slack import slack_message

    slack_message('path/to/my_message.slack', {
        'foo': Foo.objects.get(pk=17),
    }, blocks=blocks)

You can build any number of sections within the `blocks` list. For further information,
please visit `Creating rich message layouts
<https://api.slack.com/messaging/composing/layouts>`_.

Logging Exceptions to Slack
---------------------------

You can send logging messages from Django to Slack using the
``SlackExceptionHandler``:

#. Add a handler that uses the ``SlackExceptionHandler`` class to the
``LOGGING`` dictionary in your ``settings`` file::

    LOGGING = {
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'handlers': {
            'slack_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django_slack.log.SlackExceptionHandler',
            },
        },
        'loggers': {
            'django': {
                'level': 'ERROR',
                'handlers': ['slack_admins'],
            },
        },
    }

Configuration
-------------

``SLACK_TOKEN``
~~~~~~~~~~~~~~~

Default: ``None``

Your Slack authentication token. You can override on a per-message level by
specifying a ``{% block token %}{% endblock %}`` in your message templates.

See the "Tokens" section for more information.

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

``SLACK_AS_USER``
~~~~~~~~~~~~~~~~~~
Default: ``False``

Use this setting to set post the message as the authed bot user or a bot.

If SLACK_AS_USER set as True, SLACK_USERNAME setting will be ignored.

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

Default: ``https://slack.com/api/chat.postMessage``

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

Default: ``"django_slack.backends.UrllibBackend"``
(``"django_slack.backends.DisabledBackend"`` if ``settings.DEBUG``)

A string pointing to the eventual backend class that will actually send the
message to the Slack API. The default backend will send the message using the
Python ``urllib`` library.

You can use this setting to globally disable sending messages to Slack. You
may need to set this to ``django_slack.backends.DisabledBackend`` when running
tests or in your staging environment if you do not already set ``DEBUG = True``
in these environments.

If you are using Celery, the ``django_slack.backends.CeleryBackend`` backend
will ensure your messages are sent asynchronously and does not delay processing
of requests.

You can also use the supplied ``django_slack.backends.ConsoleBackend`` when
developing. Instead of actually sending the message to Slack, the console
backend just writes the emails that would be sent to standard output.

If you prefer to use Requests, please use
``django_slack.backends.RequestsBackend``.

``SLACK_BACKEND_FOR_QUEUE``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``"django_slack.backends.UrllibBackend"``
(``"django_slack.backends.DisabledBackend"`` if ``settings.DEBUG``)

If you are using a queue-based backend such as
``django_slack.backends.CeleryBackend``, this is underlying backend through
which the message will be sent.

This allows you to, for example, use the Requests library to whilst sending
your message asynchronously via Celery.

Testing
-------

You can set ``SLACK_BACKEND = django_slack.backends.TestBackend`` when testing
to store messages to inspect them later::

    from django_slack.utils import get_backend

    backend = get_backend()
    backend.reset_messages()

    # Do something that triggers the sending of a message

    messages = backend.retrieve_messages()
    assert len(messages) == 1
    assert messages[0]['text'] == expected_text
"""

from .api import slack_message
