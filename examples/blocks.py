from wolai.types.block import *
from wolai.types import *
from wolai.types.block.list import make_list
from wolai.auth import get_authed_context, get_token, refresh_token
from wolai.block import create_block, get_block_children

try:
    from local_settings import APP_ID, APP_SECRET
except ImportError:
    APP_ID = '4X96H9ovsa7pyK6xmPgBHm'
    APP_SECRET = '5086c508ef0711543ca932d375f1fb3d4222d3fd69c69f2b15e17e1c0188bddf'

PARENT_ID = '4DqJJqtV7RpJX74VE9noMB'
IMAGE = 'https://img2.baidu.com/it/u=3202947311,1179654885&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500'


def main():
    # get authed context
    app_token = get_token(APP_ID, APP_SECRET)
    refresh_token(app_token)

    ctx = get_authed_context(APP_ID, APP_SECRET)

    a = HeadingBlock(level=HeadingLevel.TWO, content=['My ', RichText(type=InlineTitleType.text,
                                                                      front_color=BlockFrontColors.pink,
                                                                      back_color=BlockBackColors.light_pink_background,
                                                                      # TODO: back_color not working
                                                                      title='Colorful API')])
    b = TextBlock(content='center!!!', text_alignment=TextAlign.center)
    c = CodeBlock(content='def main():\n    print("hello")', language='python',
                  code_setting=CodeSetting(line_number=True, link_break=True))

    d = PageBlock(icon=EmojiIcon('🐕'), page_cover=LinkCover(url=IMAGE),
                  page_setting=PageSetting(font_family=PageFontFamily.kaiti),
                  content=RichText(type=InlineTitleType.text, title='My New Page via API'))
    e = CallOutBlock(icon=EmojiIcon('🐎'), marquee_mode=True, content='🐎' * 50)

    # block_alignment = BlockAlign.center is awesome :)
    f = ImageBlock(link=IMAGE, caption='test image', block_alignment='center')
    g = ProgressBarBlock(progress=50)
    h = BookMarkBlock(link='https://baidu.com')
    i = DividerBlock()

    # create some basic blocks
    create_block(ctx, PARENT_ID, blocks=[a, b, c, d, e, f, g, h, i])

    # generate a todo_list via make_list function
    todo = [
        {'content': 'doing ...', 'task_status': 'doing'},
        {'content': 'todo 😶'},
        {'content': 'done 👌', 'task_status': 'done'}
    ]
    k = make_list(todo, TodoListProBlock)
    create_block(ctx, PARENT_ID, blocks=k)

    # get children blocks
    blocks = [i.block_instance for i in get_block_children(ctx, PARENT_ID)[0]]

    # submit children blocks to another page
    create_block(ctx, 's7gEya6cGdHQHV9vzUJYVK', blocks=blocks)


if __name__ == '__main__':
    main()
