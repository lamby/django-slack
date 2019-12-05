import json

from django.test import TestCase

from django_slack.exceptions import ChannelNotFound, MsgTooLong
from django_slack.backends import Backend


class TestOverride(TestCase):
    def test_ok_result(self):
        backend = Backend()
        backend.validate('application/json', json.dumps({'ok': True}), {})

    def test_msg_too_long_result(self):
        # Arbitrarily chosen 'simple' error
        backend = Backend()
        with self.assertRaisesRegex(
            MsgTooLong, r"msg_too_long",
        ):
            backend.validate(
                'application/json',
                json.dumps({'ok': False, 'error': 'msg_too_long'}),
                {},
            )

    def test_channel_not_found_result(self):
        backend = Backend()
        with self.assertRaisesRegex(
            ChannelNotFound, r"channel 'bad-channel' could not be found",
        ):
            backend.validate(
                'application/json',
                json.dumps({'ok': False, 'error': 'channel_not_found'}),
                {'channel': 'bad-channel'},
            )
