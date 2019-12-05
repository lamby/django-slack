import django
import unittest

from django_slack import slack_message
from django_slack.utils import get_backend


class SlackTestCase(unittest.TestCase):
    def setUp(self):
        self.backend = get_backend()
        self.backend.reset()

    def assertMessageCount(self, count):
        self.assertEqual(len(self.backend.messages), count)

    def assertMessage(self, url=None, **kwargs):
        """
        Ensure there was only one message sent with a URL and data values.
        """

        self.assertMessageCount(1)
        message = self.backend.messages[0]

        # Optionally ensure the URL.
        if url is not None:
            self.assertEqual(url, message['url'])

        # Ensure each input value in data.
        for kwarg, value in kwargs.items():
            self.assertEqual(value, message['message_data'][kwarg])


class TestEscaping(SlackTestCase):
    def test_simple_message(self):
        slack_message('test.slack', {'text': 'test'})
        self.assertMessage(text='test')

    def test_escaped(self):
        """
        Simple test of the Django escaping to illustrate problem.
        """
        slack_message('test.slack', {'text': '< > & " \''})
        if django.VERSION[0] >= 3:
            self.assertMessage(text='&lt; &gt; &amp; &quot; &#x27;')
        else:
            self.assertMessage(text='&lt; &gt; &amp; &quot; &#39;')

    def test_escape_tag(self):
        """
        Test using the escape tag, but not escaping anything.
        """
        slack_message('escape.slack', {'text': 'test'})
        self.assertMessage(text='test')

    def test_escape_chars(self):
        """
        Test the characters Slack wants escaped.

        See <https://api.slack.com/docs/formatting#how_to_escape_characters>
        """
        slack_message('escape.slack', {'text': '< > &'})
        self.assertMessage(text='&lt; &gt; &amp;')

    def test_not_escape_chars(self):
        """
        Test normal HTML escaped characters that Slack doesn't want escaped.
        """
        slack_message('escape.slack', {'text': '" \''})
        self.assertMessage(text='" \'')
