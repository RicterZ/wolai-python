import xmltodict
import codecs
import re
import hashlib
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement, NavigableString
from wolai import Wolai
from wolai.logger import logger
from wolai.types.block import *
from wolai.types.block.color import BlockFrontColors, BlockBackColors
from wolai.types.text import RichText, TextAlign
from wolai.types.block.list import make_list, BullListBlock, EnumListBlock

from local_settings import APP_ID, APP_SECRET


MATCH_HEADING = re.compile('^h([1-6])$')
BLOCK_TAGS = ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'pre', 'center', 'table', 'tr', 'tbody',
              'thead', )
INLINE_TAGS = ('span', 'b', 'strong', 'i', 'code', 'a', )

DECORATE_TAG_MAP = {
    'u': 'underline',
    'b': 'bold',
    'strong': 'bold',
    'i': 'italic',
    's': 'strikethrough',
    'code': 'inline_code',
}

BACKGROUND_COLOR = {
    'orange': BlockBackColors.vivid_tangerine_background,
    'purple': BlockBackColors.pale_purple_background,
    'green': BlockBackColors.aero_blue_background,
    'blue': BlockBackColors.uranian_blue_background,
    'red': BlockBackColors.light_pink_background,
    'yellow': BlockBackColors.blond_background,
}

FRONT_COLOR = {
    'rgb(229, 158, 37)': 'yellow',
    'rgb(24, 168, 65)': 'green',
    'rgb(26, 169, 178)': 'blue',
    'rgb(24, 133, 226)': 'blue',
    'rgb(13, 58, 153)': 'indigo',
    'rgb(87, 36, 194)': 'purple',
    'rgb(182, 41, 212)': 'pink',
    'rgb(252, 18, 51)': 'red',
    'rgb(251, 95, 44)': 'orange',
    'rgb(90, 90, 90)': 'dark_gray',
    'rgb(140, 140, 140)': 'dark_gray',
    'rgb(191, 191, 191)': 'gray',
}


def get_texts(element: Tag | NavigableString) -> list[RichText]:
    ret: list[RichText] = []

    if isinstance(element, NavigableString):
        if element.text.strip():
            ret.append(RichText(element.text))
        return ret

    style = parse_style(element)
    parent_background_color = style.get('--en-highlight', BlockBackColors.default_background)
    parent_front_color = style.get('color', BlockFrontColors.default)

    for child in element.children:
        background_color = BlockBackColors.default_background
        front_color = BlockFrontColors.default
        texts = []

        tag_name = getattr(child, 'name')

        if isinstance(child, Tag):
            grandchild = list(child.children)
            style = parse_style(child)
            background_color_name = style.get('--en-highlight', 'default')
            background_color = BACKGROUND_COLOR.get(background_color_name, parent_background_color)

            front_color_name = style.get('color', 'default')
            front_color = FRONT_COLOR.get(front_color_name, parent_front_color)

        elif isinstance(child, NavigableString):
            grandchild = [child.text]
        else:
            raise Exception(f'unhandled type {type(child)}')

        if len(grandchild) == 1 and isinstance(grandchild[0], NavigableString):
            if grandchild[0].text.strip():
                texts = [RichText(grandchild[0].text)]
        else:
            texts = get_texts(child)

        # just do the style decoration
        if tag_name in DECORATE_TAG_MAP.keys():
            for item in texts:
                setattr(item, DECORATE_TAG_MAP.get(tag_name), True)

        elif tag_name == 'br':
            texts.append(RichText('\n'))

        else:
            pass

        if not texts:
            continue

        for item in texts:
            if background_color is None:
                background_color = parent_background_color

            if front_color is None:
                front_color = parent_front_color

            if item.back_color == BlockBackColors.default_background:
                setattr(item, 'back_color', background_color)

            if item.front_color == BlockFrontColors.default:
                setattr(item, 'front_color', front_color)

        ret.extend(texts)

    return ret


def parse_style(element: Tag) -> dict:
    ret = {}

    style = element.attrs.get('style', '')
    for line in style.split(';'):
        line = line.strip()
        if not line or ':' not in line:
            continue

        k, v = map(lambda s: s.strip(), line.split(':', 1))
        ret[k] = v

    return ret


def has_block_tag(element: Tag) -> bool:
    for tag in BLOCK_TAGS:
        if element.findAll(tag):
            return True
    return False


def process_block_tags(element: Tag) -> Block | None:
    tag_name = getattr(element, 'name')
    style = parse_style(element)

    if tag_name == 'div':
        block = TextBlock(get_texts(element))

    elif tag_name == 'pre':
        block = CodeBlock(language='php', content=element.text)

    elif MATCH_HEADING.findall(tag_name):
        level = int(MATCH_HEADING.findall(tag_name)[0])
        if level >= 4:
            level = 4
        block = HeadingBlock(level=level, content=element.text)

    elif tag_name == 'center':
        block = TextBlock(content=get_texts(element), text_alignment=TextAlign.center)

    else:
        block = TextBlock(get_texts(element))

    if style.get('text-align') == 'center':
        block.text_alignment = TextAlign.center

    return block


def elements2blocks(element: PageElement | Tag | NavigableString, image_table: dict = None) -> list[Block]:
    blocks: list[Block] = []
    style = parse_style(element)

    for child in element.children:
        if not isinstance(child, Tag):
            continue

        tag_name = getattr(child, 'name')
        if style.get('--en-codeblock') == 'true':
            texts = get_texts(element)
            code = ''
            for item in texts:
                code += f'{item.title}\n'

            blocks.append(CodeBlock(content=code, language='php'))
            break

        else:
            if tag_name in ('ul', 'ol'):
                items = [{'content': get_texts(item)} for item in child.findAll('li')]
                if tag_name == 'ul':
                    if parse_style(child).get('--en-todo') == 'true':
                        items = [{
                            'content': get_texts(item),
                            'checked': parse_style(item).get('--en-checked') == 'true'
                        } for item in child.findAll('li')]

                        blocks.extend(make_list(items, TodoListBlock))
                    else:
                        blocks.extend(make_list(items, BullListBlock))
                elif tag_name == 'ol':
                    blocks.extend(make_list(items, EnumListBlock))

            elif tag_name == 'en-media':
                if image_table:
                    url = image_table.get(child.attrs['hash'], 'https://www.wolai.com/notexists')
                    blocks.append(ImageBlock(link=url))

            elif tag_name == 'hr':
                blocks.append(DividerBlock())

            elif tag_name == 'table':
                code_block = child.findAll('code')
                if code_block:
                    code = ''
                    for line in code_block:
                        print(line)
                        code += f'{line.text}\n'
                    blocks.append(CodeBlock(content=code, language='php'))
                else:
                    raise NotImplementedError

            elif tag_name in BLOCK_TAGS and not has_block_tag(child):
                blocks.append(process_block_tags(child))

            elif has_block_tag(child):
                blocks.extend(elements2blocks(child, image_table=image_table))

            elif tag_name is None or tag_name in INLINE_TAGS or tag_name == 'br':
                if child.text.strip():
                    blocks.append(TextBlock(get_texts(child)))

            else:
                logger.info(f'unhandled tag <{tag_name}>: {child}')

    return blocks


def fix_write_chars(content: str) -> str:
    content = content.replace('&nbsp;', ' ')
    content = content.replace('\xa0', ' ')
    return content


def upload_images(image_data: bytes) -> str:
    return 'https://baidu.com/a.jpg'


def main():
    wolai_obj = Wolai(app_id=APP_ID, app_secret=APP_SECRET, page_id='h6J51UmA3KJYHQ1QSjDteS')

    with open('rop.enex', 'rb') as f:
        data = xmltodict.parse(f.read())

        notes = data['en-export']['note']
        if not isinstance(notes, list):
            notes = [notes]

        for note in notes:
            logger.info(f'processing note: {note["title"]} ...')

            if note['title'] != '一步一步学ROP之linux_x86篇 | WooYun知识库':
                continue

            content = BeautifulSoup(fix_write_chars(note['content']), features='xml').find('en-note')

            image_table = {}
            resources = note.get('resource', [])
            if isinstance(resources, dict):
                resources = [resources]

            for i in resources:
                image_data = codecs.decode(i['data']['#text'].encode(), 'base64')
                url = upload_images(image_data)
                logger.info(f'image uploaded successfully: {url}')
                image_table[hashlib.md5(image_data).hexdigest()] = url

            blocks = elements2blocks(content, image_table=image_table)
            note_page = wolai_obj.create_page(note['title'])
            note_page.create_blocks(blocks)


def main2():
    wolai_obj = Wolai(app_id=APP_ID, app_secret=APP_SECRET, page_id='h6J51UmA3KJYHQ1QSjDteS')
    content = BeautifulSoup('<p>abc<a href=def>def</a>ghi<span>span</span><code>code</code></p>', 'html.parser')
    blocks = elements2blocks(content, image_table=None)

    note_page = wolai_obj.create_page('Test')
    note_page.create_blocks(blocks)


if __name__ == '__main__':
    main()
