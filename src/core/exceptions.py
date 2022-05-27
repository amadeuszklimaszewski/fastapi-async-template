class APIException(Exception):
    pass


class AlreadyExists(APIException):
    pass


class AuthException(APIException):
    pass


class InvalidCredentials(AuthException):
    pass
