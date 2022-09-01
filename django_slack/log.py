import copy
import logging

from django.conf import settings
from django.views.debug import get_exception_reporter_class

from . import slack_message


class SlackExceptionHandler(logging.Handler):
    """
    An exception log handler that sends log entries to a Slack channel.
    """

    def __init__(self, **kwargs):
        # Pop any kwargs that shouldn't be passed into the Slack message
        # attachment here.
        self.template = kwargs.pop('template', 'django_slack/exception.slack')

        self.kwargs = kwargs
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            request = record.request

            internal = (
                'internal'
                if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                else 'EXTERNAL'
            )

            subject = '{} ({} IP): {}'.format(
                record.levelname, internal, record.getMessage(),
            )
        except Exception:
            subject = '{}: {}'.format(record.levelname, record.getMessage(),)
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy.copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = get_exception_reporter_class(request)(request, is_email=True, *exc_info)

        try:
            tb = reporter.get_traceback_text()
        except:
            tb = "(An exception occured when getting the traceback text)"

            if reporter.exc_type:
                tb = (
                    "{} (An exception occured when rendering the "
                    "traceback)".format(reporter.exc_type.__name__)
                )

        message = "{}\n\n{}".format(self.format(no_exc_record), tb)

        colors = {
            'ERROR': 'danger',
            'WARNING': 'warning',
            'INFO': 'good',
        }

        attachments = {
            'title': subject,
            'text': message,
            'color': colors.get(record.levelname, '#AAAAAA'),
        }

        attachments.update(self.kwargs)
        self.send_message(
            self.template,
            {'text': subject},
            self.generate_attachments(**attachments),
        )

    def generate_attachments(self, **kwargs):
        """
        Hook to override attachments.
        """
        return [kwargs]

    def send_message(self, *args, **kwargs):
        """
        Hook to update the message before sending.
        """
        return slack_message(*args, **kwargs)

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length. RFC 2822's hard limit is
        998 characters per line. So, minus "Subject: " the actual subject must
        be no longer than 989 characters.
        """

        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')

        return formatted_subject[:989]
