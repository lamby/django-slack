class SlackException(ValueError):
    pass

class ChannelNotFound(SlackException):
    pass

class IsArchived(SlackException):
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
    'msg_too_long': MsgTooLong,
    'no_text': NoText,
    'rate_limited': RateLimited,
    'not_authed': NotAuthed,
    'invalid_auth': InvalidAuth,
    'token_revoked': TokenRevoked,
    'account_inactive': AccountInactive,
    'user_is_bot': UserIsBot,
}
