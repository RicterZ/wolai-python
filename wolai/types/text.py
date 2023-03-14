import typing

from wolai.types.enum import AutoName, auto, Base
from wolai.types.block.color import BlockFrontColors, BlockBackColors


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
    front_color: BlockFrontColors = None
    back_color: BlockBackColors = None

    def __init__(self, title: str, bold: bool = False, italic: bool = False, type: InlineTitleType | str = 'text',
                 underline: bool = False, highlight: bool = False, strikethrough: bool = False,
                 inline_code: bool = False, front_color: BlockFrontColors | str = BlockFrontColors.default,
                 back_color: BlockBackColors | str = BlockBackColors.default_background):

        if isinstance(type, str):
            type = InlineTitleType[type]

        self.type = type
        self.title = title
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.highlight = highlight
        self.strikethrough = strikethrough
        self.inline_code = inline_code

        if isinstance(front_color, str):
            front_color = BlockFrontColors[front_color]
        if isinstance(back_color, str):
            back_color = BlockBackColors[back_color]

        self.front_color = front_color
        self.back_color = back_color

    def __getattribute__(self, item):
        ret = super().__getattribute__(item)
        if item == '__dict__':
            if self.back_color != BlockBackColors.default_background:
                if 'front_color' in ret:
                    del ret['front_color']

        return ret


CreateRichText = typing.TypeVar('CreateRichText', str, RichText, None, list[str | RichText])
