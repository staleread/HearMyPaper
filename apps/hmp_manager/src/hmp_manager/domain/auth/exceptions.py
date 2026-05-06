class AuthError(Exception):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidChallengeError(AuthError):
    pass


class AuthenticationFailedError(AuthError):
    pass
