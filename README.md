# wolai-python
Unofficial wolai python SDK, only supports python 3.10+.

### Installation

```bash
pip3 install wolai-python
```

For development:
```bash
poetry shell
poetry install
```

### Usage

#### 1. Get authed context
```python
from wolai.auth import get_authed_context

APP_ID, APP_SECRET = 'xxx', 'xxxxx'
ctx = get_authed_context(APP_ID, APP_SECRET)
```

#### 2. Create blocks
```python
from wolai.types.block import *
from wolai.types import *
from wolai.block import create_block

PARENT_ID = 'xxx'
ctx = ...

a = HeadingBlock(level=HeadingLevel.TWO, content=['My ', RichText(type=InlineTitleType.text,
                                                                  front_color=BlockFrontColors.pink,
                                                                  back_color=BlockBackColors.light_pink_background,
                                                                  title='Colorful API')])
b = TextBlock(content='center!!!', text_alignment=TextAlign.center)
c = CodeBlock(content='def main():\n    print("hello")', language='python',
              code_setting=CodeSetting(line_number=True, link_break=True))
create_block(ctx, PARENT_ID, blocks=[a, b, c])
```

#### 3. Use `Wolai` class
```python
from wolai import Wolai

APP_ID, APP_SECRET = 'xxx', 'xxx'
PARENT_ID = 'xxx'

wolai_obj = Wolai(app_id=APP_ID, app_secret=APP_SECRET, page_id=PARENT_ID)
note_page = wolai_obj.create_page('Test')
note_page.create_blocks(...)
```