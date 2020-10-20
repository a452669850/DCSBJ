class SkError(Exception):
    msg: str = ''
    errno: int = 0

    def __init__(self, errno=0, msg=''):
        super(SkError, self).__init__(msg)
        self.errno = errno
        self.msg = msg


class VarNotFound(SkError):
    errno = 404

    def __init__(self, name):
        SkError.__init__(self, msg=name)


class UnsupportedType(SkError):
    errno = 415
    msg = ''


VAR_CFG_ERROR = 101
UNSUPPORTED_TYPE = 102
READ_ONLY = 103
NETWORK_ERROR = 104
PROTOCOL_ERROR = 105
VAR_NOT_FOUND = 106
