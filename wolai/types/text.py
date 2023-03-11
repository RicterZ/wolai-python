import typing

from wolai.types.enum import AutoName, auto, Base
from wolai.types.block.color import BlockFrontColor, BlockBackColor


class TextAlign(AutoName):
    left = auto()
    center = auto()
    right = auto()


class InlineTitleType(AutoName):
    text = auto()
    link = auto()
    bi_link = auto()
    comment = auto()
    equation = auto()
    font_awesome = auto()
    mention = auto()
    note = auto()
    footnote = auto()


class RichText(Base):
    type: InlineTitleType = None
    title: str = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    highlight: bool = False
    strikethrough: bool = False
    inline_code: bool = False
    front_color: BlockFrontColor = None
    back_color: BlockBackColor = None

    def __init__(self, type_: InlineTitleType, title: str, bold: bool = False, italic: bool = False,
                 underline: bool = False, highlight: bool = False, strikethrough: bool = False,
                 inline_code: bool = False, front_color: BlockFrontColor = BlockFrontColor.default,
                 back_color: BlockBackColor = BlockBackColor.default):
        self.type = type_
        self.title = title
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.highlight = highlight
        self.strikethrough = strikethrough
        self.inline_code = inline_code
        self.front_color = front_color
        self.back_color = back_color


CreateRichText = typing.TypeVar('CreateRichText', str, RichText, None, list[str, RichText])
