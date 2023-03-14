from wolai.auth import get_authed_context
from wolai.block import create_block, get_block, get_block_children
from wolai.types.block import Block
from wolai.types.block.page import PageBlock, PageSetting
from wolai.types.cover import Cover
from wolai.types.icon import Icon


class Wolai:
    app_id: str = None
    app_secret: str = None
    parent_page_id: str = None

    ctx: callable = None

    def init_context(self):
        self.ctx = get_authed_context(self.app_id, self.app_secret)

    def __init__(self, app_id: str = None, app_secret: str = None, page_id: str = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.parent_page_id = page_id
        self.init_context()

    def create_page(self, title: str, parent_page_id: str = None, page_setting: PageSetting = None,
                    cover: Cover = None, icon: Icon = None):
        if parent_page_id is None:
            parent_page_id = self.parent_page_id

        page = PageBlock(content=title, page_setting=page_setting, cover=cover, icon=icon)
        page_id = self.create_blocks(page, parent_page_id=parent_page_id)
        return WolaiPage(ctx=self.ctx, page_id=page_id)

    def create_blocks(self, blocks: list[Block] | Block, parent_page_id: str = None) -> str:
        if parent_page_id is None:
            parent_page_id = self.parent_page_id

        return create_block(ctx=self.ctx, parent_id=parent_page_id, blocks=blocks)


class WolaiPage(Wolai):

    def init_context(self):
        pass

    def __init__(self, ctx: callable, page_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.parent_page_id = page_id
