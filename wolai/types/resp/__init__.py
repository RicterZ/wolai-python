import json
import typing
from collections import ChainMap

from wolai.types.block import BlockType, BlockAlign, Block
from wolai.types.text import RichText, TextAlign
from wolai.types.block.color import BlockFrontColor, BlockBackColor
from wolai.types.database import DatabaseRowData
from wolai.exceptions import WolaiEnumTypeException
from wolai.encoder import to_json
from wolai.logger import logger


def all_subclasses(cls) -> set:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def all_annotations(cls) -> ChainMap:
    """Returns a dictionary-like ChainMap that includes annotations for all
       attributes defined in cls or inherited from superclasses."""
    return ChainMap(*(c.__annotations__ for c in cls.__mro__ if '__annotations__' in c.__dict__))


class Response:
    def __init__(self, *args, **kwargs):
        self._unused_param = {}

        for k, v in kwargs.items():
            t = self.__annotations__.get(k)
            if t is None:
                self._unused_param[k] = v
                continue

            if typing.get_origin(t) == list:
                list_args = typing.get_args(t)
                if len(list_args) > 1:
                    raise Exception('only 1 type of list supported')

                if list_args[0].__module__ != 'builtins':
                    cls = list_args[0]
                    v = [cls(**i) for i in v]
                else:
                    v = t(v)

            elif isinstance(v, dict):
                v = t(**v)
            else:
                v = t(v)

            setattr(self, k, v)


class Children(Response):
    ids: list[str] = None
    api_url: str = None


class BlockFormat(Response):
    block_instance: Block = None

    id: str = None
    parent_id: str = None
    parent_type: str = None
    page_id: str = None
    children: Children = None
    type: BlockType = None
    content: list[RichText] = None
    version: int = None
    created_by: str = None
    created_at: int = None
    edited_by: str = None
    edited_at: int = None
    block_front_color: BlockFrontColor = None
    block_back_color: BlockBackColor = None
    text_alignment: TextAlign = None
    block_alignment: BlockAlign = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        block_cls = None
        for cls in all_subclasses(Block):
            if cls.type is None:
                try:
                    block_type = BlockType[cls.__name__[:-5].lower()]
                except WolaiEnumTypeException:
                    continue
            else:
                block_type = cls.type

            if block_type == self.type:
                block_cls = cls
                break

        if block_cls is None:
            # TODO: unsupported block type
            logger.debug(f'unsupported block type {self.type}')

        for k, v in self._unused_param.items():
            t = all_annotations(block_cls).get(k)
            if t is None:
                # TODO: undocumented field ...
                logger.debug(f'unknown field {k} of {block_cls.__name__}')

        self._unused_param.update(self.__dict__)
        setattr(self, 'block_instance', block_cls(**self._unused_param))


class DatabaseFormat(Response):
    column_order: list[str] = None
    rows: list[DatabaseRowData] = None
