# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-20
#
# ====================================================


from typing import Dict, List, Tuple, Any, Optional, Iterator, Union, overload
from _typeshed import Self


class auto(object):
    pass


class EnumMeta(type):
    _flag: int
    __members__: Dict[str, Any]
    _restrict_type: Optional[type]
    def __new__(
        metacls: type[Self],
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
        restrict_type: Optional[type] = None,
    ) -> Self: ...
    def __setattr__(cls, name: str, value: Any) -> None: ...
    def __delattr__(cls, name: str) -> None: ...
    def __contains__(cls, member: Any) -> bool: ...
    def __len__(cls) -> int: ...
    def __iter__(cls: type[Self]) -> Iterator[Self]: ...
    @overload
    def __getitem__(cls, item: type) -> type[Enum]: ...
    @overload
    def __getitem__(cls, item: str) -> Any: ...
    def __gen_auto_value__(cls) -> Union[str, int]: ...


class Enum(metaclass=EnumMeta):
    __name: str
    __value: Any
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
