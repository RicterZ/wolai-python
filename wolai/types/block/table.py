from wolai.types.block import Block, BlockType
from wolai.types.text import CreateRichText


class TableSetting:
    has_header: bool = False

    def __init__(self, has_header: bool = False):
        self.has_header = has_header


class SimpleTableBlock(Block):
    type: BlockType = BlockType.simple_table
    table_content: list[list[CreateRichText]] = None
    table_setting: TableSetting = None
    caption: str = None

    def __init__(self, table_content: list[list[CreateRichText]] = None,
                 table_setting: TableSetting = None, caption: str = None, **kwargs):
        super().__init__(**kwargs)
        self.table_content = table_content
        self.table_setting = table_setting
        self.caption = caption
