class SlackException(ValueError):
    def __init__(self, message, message_data):
        super(SlackException, self).__init__(message)
        self.message_data = message_data


class ChannelNotFound(SlackException):
    def __str__(self):
        # Override base __str__ to ensure we include the channel name in the
        # error message
        return u"{}: channel '{}' could not be found".format(
            self.__class__.__name__, self.message_data['channel'],
        )


class IsArchived(SlackException):
    pass


class FatalError(SlackException):
    pass


class MsgTooLong(SlackException):
    pass


class NoText(SlackException):
    pass


class RateLimited(SlackException):
    pass


class NotAuthed(SlackException):
    pass


class InvalidAuth(SlackException):
    pass


class TokenRevoked(SlackException):
    pass


class AccountInactive(SlackException):
    pass


class UserIsBot(SlackException):
    pass


LABEL_TO_EXCEPTION = {
    'channel_not_found': ChannelNotFound,
    'is_archived': IsArchived,
    'fatal_error': FatalError,
    'msg_too_long': MsgTooLong,
    'no_text': NoText,
    'rate_limited': RateLimited,
    'not_authed': NotAuthed,
    'invalid_auth': InvalidAuth,
    'token_revoked': TokenRevoked,
    'account_inactive': AccountInactive,
    'user_is_bot': UserIsBot,
}
