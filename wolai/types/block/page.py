from wolai.types.block import Block
from wolai.types.text import CreateRichText
from wolai.types.icon import Icon
from wolai.types.cover import Cover
from wolai.types.enum import AutoName, auto


class PageFontFamily(AutoName):
    default = auto()
    simsun = auto()
    kaiti = auto()


class PageLineLeading(AutoName):
    default = auto()
    loose = auto()
    compact = auto()


class PageSetting:
    is_full_width: bool = False
    is_small_text: bool = False
    has_floating_catalog: bool = False
    font_family: PageFontFamily = None
    line_spacing: PageLineLeading = None

    def __init__(self, is_full_width: bool = False, is_small_text: bool = False, has_floating_catalog: bool = False,
                 font_family: PageFontFamily = PageFontFamily.default,
                 line_spacing: PageLineLeading = PageLineLeading.default):
        self.is_small_text = is_small_text
        self.is_full_width = is_full_width
        self.has_floating_catalog = has_floating_catalog
        self.font_family = font_family
        self.line_spacing = line_spacing


class PageBlock(Block):
    icon: Icon = None
    page_cover: Cover = None
    page_setting: PageSetting = None
    content: CreateRichText = None

    def __init__(self, icon: Icon = None, page_cover: Cover = None, page_setting: PageSetting = None,
                 content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.page_cover = page_cover
        self.page_setting = page_setting
        self.content = content

