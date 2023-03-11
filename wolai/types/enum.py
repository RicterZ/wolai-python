from enum import Enum, EnumMeta, auto
from wolai.exceptions import WolaiEnumTypeException


auto = auto


class Base:
    pass


class _EnumMeta(EnumMeta):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            raise WolaiEnumTypeException(f'unknown value "{item}" of enum {self.__name__}')


class AutoName(Enum, metaclass=_EnumMeta):
    @staticmethod
    def _generate_next_value_(name, *args, **kwargs):
        return name
