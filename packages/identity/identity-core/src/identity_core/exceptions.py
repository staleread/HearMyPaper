class IdentityError(Exception):
    pass


class UserNotFoundError(IdentityError):
    pass


class InvalidChallengeError(IdentityError):
    pass


class AuthenticationFailedError(IdentityError):
    pass


class UserAlreadyExistsError(IdentityError):
    pass


class IdentityCollisionError(IdentityError):
    pass


class InvalidPublicKeyError(IdentityError):
    pass
