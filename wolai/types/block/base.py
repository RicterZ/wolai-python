from wolai.types.enum import AutoName, Base, auto
from wolai.types.text import TextAlign
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

    def __init__(self, text_alignment: TextAlign | str = TextAlign.left,
                 block_alignment: BlockAlign | str = BlockAlign.left, **kwargs):

        if self.type is None:
            self.type = BlockType[self.__class__.__name__[:-5].lower()]

        if isinstance(text_alignment, str):
            text_alignment = TextAlign[text_alignment]

        self.text_alignment = text_alignment

        if isinstance(block_alignment, str):
            block_alignment = BlockAlign[block_alignment]

        self.block_alignment = block_alignment


