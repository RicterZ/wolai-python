from wolai.types.text import CreateRichText
from wolai.types.block import Block, BlockType
from wolai.types.icon import Icon
from wolai.exceptions import WolaiValueException


class TextBlock(Block):
    content: CreateRichText = None

    def __init__(self, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.content = content


class QuoteBlock(Block):
    content: CreateRichText = None

    def __init__(self, content: CreateRichText, **kwargs):
        super().__init__(**kwargs)
        self.content = content


class CallOutBlock(Block):
    icon: Icon = None
    marquee_mode: bool = False
    content: CreateRichText = None

    def __init__(self, icon: Icon = None, marquee_mode: bool = False, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.marquee_mode = marquee_mode
        self.content = content


class DividerBlock(Block):
    pass


class ProgressBarBlock(Block):
    progress: int = 0
    auto_mode: bool = False
    hide_number: bool = False
    type = BlockType.progress_bar

    def __init__(self, progress: int = 0, auto_mode: bool = False, hide_number: bool = False, **kwargs):
        super().__init__(**kwargs)
        if progress > 100:
            raise WolaiValueException(f'invalid value {progress} of progress bar')

        self.progress = progress
        self.auto_mode = auto_mode
        self.hide_number = hide_number


class BookMarkBlock(Block):
    link: str = None

    def __init__(self, link: str = None, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get('bookmark_source') is not None and link is None:
            link = kwargs.get('bookmark_source')

        self.link = link


class EquationBlock(Block):
    type = BlockType.block_equation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EmbedBlock(Block):
    original_link: str = None
    embed_link: str = None

    def __init__(self, original_link: str = None, embed_link: str = None, **kwargs):
        super().__init__(**kwargs)
        self.original_link = original_link
        self.embed_link = embed_link
