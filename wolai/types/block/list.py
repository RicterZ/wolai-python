from wolai.types.block import Block, BlockType
from wolai.types.enum import AutoName, auto
from wolai.types.block.block import TextBlock
from wolai.types.text import CreateRichText


class ListBlock(Block):
    content: CreateRichText = None


def make_list(items: list[dict], cls: ListBlock.__class__) -> list[Block]:
    ret = [cls(**i) for i in items]
    ret.append(TextBlock())
    return ret


class EnumListBlock(ListBlock):
    type = BlockType.enum_list

    def __init__(self, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.content = content


class TodoListBlock(ListBlock):
    type = BlockType.todo_list
    checked: bool = False

    def __init__(self, content: CreateRichText = None, checked: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.checked = checked


class TodoListProStatus(AutoName):
    todo = auto()
    doing = auto()
    done = auto()
    cancel = auto()


class TodoListProBlock(ListBlock):
    task_status: TodoListProStatus = False
    type = BlockType.todo_list_pro

    def __init__(self, content: CreateRichText = None, task_status: TodoListProStatus | str = TodoListProStatus.todo,
                 **kwargs):
        super().__init__(**kwargs)
        self.content = content
        if isinstance(task_status, str):
            task_status = TodoListProStatus[task_status]

        self.task_status = task_status


class BullListBlock(ListBlock):
    type = BlockType.bull_list

    def __init__(self, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.content = content


class ToggleListBlock(ListBlock):
    type = BlockType.toggle_list

    def __init__(self, content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
