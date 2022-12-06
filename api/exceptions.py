class AOCException(Exception):
    pass


class AuthenticationException(AOCException):
    pass


class NotLoggedInException(AOCException):
    pass
