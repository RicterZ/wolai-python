from wolai.types.enum import AutoName, Base, auto
from wolai.types.text import TextAlign
from wolai.types.block.color import BlockBackColors, BlockFrontColors
from wolai.exceptions import WolaiEnumTypeException


class BlockAlign(AutoName):
    left = auto()
    center = auto()
    right = auto()


class BlockType(AutoName):
    row = auto()
    column = auto()
    text = auto()
    page = auto()
    code = auto()
    file = auto()
    embed = auto()
    video = auto()
    audio = auto()
    image = auto()
    quote = auto()
    callout = auto()
    divider = auto()
    database = auto()
    progress_bar = auto()
    bookmark = auto()
    heading = auto()
    enum_list = auto()
    todo_list = auto()
    todo_list_pro = auto()
    bull_list = auto()
    toggle_list = auto()
    simple_table = auto()
    block_equation = auto()
    template_button = auto()
    meeting = auto()
    reference = auto()


class Block(Base):
    type: BlockType = None
    text_alignment: TextAlign = None
    block_alignment: BlockAlign = None
    block_back_color: BlockBackColors = None
    block_front_color: BlockFrontColors = None

    def __init__(self, text_alignment: TextAlign | str = TextAlign.left,
                 block_alignment: BlockAlign | str = BlockAlign.left,
                 block_front_color: BlockFrontColors = BlockFrontColors.default,
                 block_back_color: BlockBackColors = BlockBackColors.default_background, **kwargs):

        if self.type is None:
            self.type = BlockType[self.__class__.__name__[:-5].lower()]

        if isinstance(text_alignment, str):
            text_alignment = TextAlign[text_alignment]

        if isinstance(block_alignment, str):
            block_alignment = BlockAlign[block_alignment]

        if isinstance(block_front_color, str):
            block_front_color = BlockFrontColors[block_front_color]

        if isinstance(block_back_color, str):
            block_back_color = BlockBackColors[block_back_color]

        self.block_alignment = block_alignment
        self.text_alignment = text_alignment
        self.block_back_color = block_back_color
        self.block_front_color = block_front_color

    def __getattribute__(self, item):
        ret = super().__getattribute__(item)
        if item == '__dict__':
            if self.block_back_color != BlockBackColors.default_background:
                if 'block_front_color' in ret:
                    del ret['block_front_color']

        return ret
