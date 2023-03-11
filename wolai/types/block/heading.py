import typing

from enum import Enum
from wolai.types.block import Block
from wolai.types.text import CreateRichText


class HeadingLevel(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


HeadingLevelType = typing.TypeVar('HeadingLevelType', HeadingLevel, int)


class HeadingBlock(Block):
    level: HeadingLevelType = None
    toggle: bool = False
    content: CreateRichText = None

    def __init__(self, level: HeadingLevelType | int, toggle: bool = False, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(level, int):
            # TODO: the response of the level is a string
            level = HeadingLevel._value2member_map_[level]

        self.level = level
        self.toggle = toggle
        self.content = content

