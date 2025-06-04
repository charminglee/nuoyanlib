# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Dict, List, Tuple, Any, Optional, Iterator, Union, overload, Type
from _typeshed import Self


class EnumMeta(type):
    __flag__: int
    __members__: Dict[str, Any]
    _restrict_type: Optional[type]
    def __new__(
        metacls: Type[Self],
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
        restrict_type: Optional[type] = None,
    ) -> Self: ...
    def __setattr__(cls, name: str, value: Any) -> None: ...
    def __delattr__(cls, name: str) -> None: ...
    def __contains__(cls, member: Any) -> bool: ...
    def __len__(cls) -> int: ...
    def __iter__(cls: Type[Self]) -> Iterator[Self]: ...
    @overload
    def __getitem__(cls, item: type) -> Type[Enum]: ...
    @overload
    def __getitem__(cls, item: str) -> Any: ...
    def __gen_auto_value__(cls, name: Optional[str] = None) -> Union[str, int]: ...


class Enum(metaclass=EnumMeta):
    __name: str
    __value: Any
    __hash: int
    class auto(object): ...
    def __init__(self, name: str, value: Any) -> None: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> Any: ...


def search_data(data: Any, lst: list) -> bool: ...


ENTITY_LIST: List[Optional[int, str, str, int]]
MOB_LIST: List[Tuple[int, str, str, int, bool]]
FRIENDLY_MOB_LIST: List[Tuple[int, str, str, int]]
HOSTILE_MOB_LIST: List[Tuple[int, str, str, int]]
ATTACKABLE_MOB_LIST: List[Tuple[int, str, str, int]]
ENTITY_ID_DICT: Dict[int, int]
EFFECT_DICT: Dict[str, str]
BIOME_DICT: Dict[str, str]
STRUCTURE_DICT: Dict[int, Tuple[str, str]]
BLOCK_LIST: List[str]
ITEM_LIST: List[str]
