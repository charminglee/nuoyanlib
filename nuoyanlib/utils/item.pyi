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


from typing import Tuple, List, Optional
from mod.common.minecraftEnum import ItemPosType as _ItemPosType
from .._core._types._typing import ITuple2


def deepcopy_item_dict(item_dict: Optional[dict]) -> Optional[dict]: ...
def gen_item_dict(
    newItemName: str,
    newAuxValue: str = 0,
    count: str = 1,
    showInHand: bool = True,
    enchantData: Optional[List[ITuple2]] = None,
    modEnchantData: Optional[List[Tuple[str, int]]] = None,
    customTips: str = "",
    extraId: str = "",
    userData: Optional[dict] = None,
    durability: int = 0,
    itemName: str = "",
    auxValue: int = 0,
) -> Optional[dict]: ...
def get_item_count(player_id: str, name: str, aux: int = -1) -> int: ...
def set_namespace(name: str, namespace: str = "minecraft") -> str: ...
def is_same_item(item_dict1: dict, item_dict2: dict) -> bool: ...
def are_same_item(item: dict, *other_item: dict) -> bool: ...
def is_empty_item(item: dict, zero_is_emp: bool = True) -> bool: ...
def get_max_stack(item: dict) -> int: ...
