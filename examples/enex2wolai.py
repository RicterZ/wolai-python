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
from wolai.types.text import RichText
from wolai.types.block.list import make_list, BullListBlock, EnumListBlock

from local_settings import APP_ID, APP_SECRET


MATCH_HEADING = re.compile('^h([1-6])$')
BLOCK_TAGS = ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'pre', )
INLINE_TAGS = ('span', 'b', 'strong', 'i', 'code', 'a', )


def get_texts(element: PageElement | Tag | NavigableString) -> list[RichText]:
    ret: list[RichText] = []

    if isinstance(element, NavigableString):
        if element.text.strip():
            ret.append(RichText(element.text))
        return ret

    for child in element.children:
        texts = []
        tag_name = getattr(child, 'name')

        if isinstance(child, Tag):
            grandchild = list(child.children)
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
        if tag_name == 'i':
            for item in texts:
                setattr(item, 'italic', True)
        elif tag_name in ('strong', 'b'):
            for item in texts:
                setattr(item, 'bold', True)
        elif tag_name == 'span' or tag_name is None:
            # just a container
            pass
        elif tag_name == 'br':
            texts.append(RichText('\n'))
        elif tag_name == 'code':
            for item in texts:
                setattr(item, 'inline_code', True)
        else:
            pass

        if not texts:
            continue

        ret.extend(texts)

    return ret


def parse_style(style: str) -> dict:
    ret = {}
    for line in style.split(';'):
        line = line.strip()
        if not line or ':' not in line:
            continue

        k, v = map(lambda s: s.strip(), line.split(':', 2))
        ret[k] = v

    return ret


def has_block_tag(element: Tag) -> bool:
    for tag in BLOCK_TAGS:
        if element.findAll(tag):
            return True
    return False


def elements2blocks(element: PageElement | Tag | NavigableString, image_table: dict = None) -> list[Block]:
    blocks: list[Block] = []
    for child in element.children:
        tag_name = getattr(child, 'name')

        if isinstance(child, Tag) and tag_name in BLOCK_TAGS and has_block_tag(child):
            blocks.extend(elements2blocks(child, image_table=image_table))

        elif isinstance(child, Tag):
            if tag_name == 'div':
                style = parse_style(child.attrs.get('style', ''))
                texts = get_texts(child)
                if not texts:
                    continue

                if style.get('--en-codeblock') == 'true':
                    code = ''
                    for item in texts:
                        code += f'{item.title}\n'
                    blocks.append(CodeBlock(content=code, language='php'))
                else:
                    blocks.append(TextBlock(texts))

            elif tag_name in ('ul', 'ol'):
                items = [{'content': get_texts(item)} for item in child.findAll('li')]
                if tag_name == 'ul':
                    blocks.extend(make_list(items, BullListBlock))
                elif tag_name == 'ol':
                    blocks.extend(make_list(items, EnumListBlock))

            elif tag_name == 'en-media':
                if image_table:
                    url = image_table.get(child.attrs['hash'], 'https://www.wolai.com/notexists')
                    blocks.append(ImageBlock(link=url))

            elif tag_name == 'hr':
                blocks.append(DividerBlock())

            elif tag_name is None or tag_name in INLINE_TAGS:
                if child.text.strip():
                    blocks.append(TextBlock(get_texts(child)))

            elif MATCH_HEADING.findall(tag_name):
                level = int(MATCH_HEADING.findall(tag_name)[0])
                if level >= 4:
                    level = 4
                blocks.append(HeadingBlock(level=level, content=child.text))

            elif tag_name == 'pre':
                blocks.append(CodeBlock(language='php', content=child.text))

            elif tag_name in 'br':
                continue

            elif tag_name == 'table':
                pass

            elif tag_name in BLOCK_TAGS:
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

    with open('Pwnable.enex', 'rb') as f:
        data = xmltodict.parse(f.read())

        notes = data['en-export']['note']
        if not isinstance(notes, list):
            notes = [notes]

        for note in notes:
            logger.info(f'processing note: {note["title"]} ...')

            content = BeautifulSoup(fix_write_chars(note['content']), features='xml').find('en-note')

            image_table = {}
            for i in note['resource']:
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

    print(blocks)
    note_page = wolai_obj.create_page('Test')
    note_page.create_blocks(blocks)


if __name__ == '__main__':
    main2()
