class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class UserAlreadyExistsError(UserError):
    pass


class IdentityCollisionError(UserError):
    pass


class InvalidPublicKeyError(UserError):
    pass
