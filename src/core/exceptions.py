from shutil import ExecError


class APIException(Exception):
    pass


class AlreadyExists(APIException):
    pass


class AuthException(APIException):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidJWTUser(Exception):
    pass
