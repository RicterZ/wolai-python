class WolaiException(Exception):
    pass


class WolaiTokenException(WolaiException):
    pass


class WolaiRequestException(WolaiException):
    pass


class WolaiEnumTypeException(WolaiException):
    pass


class WolaiValueException(WolaiException):
    pass
