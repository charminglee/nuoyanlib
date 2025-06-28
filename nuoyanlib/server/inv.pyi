# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-19
|
| ==============================================
"""


from typing import List, Union, Optional
from mod.common.minecraftEnum import ItemPosType
from .._core._types._typing import ItemDict, STuple


def set_items_to_item_grid(player_id: str, key: str, item_dict_list: List[Optional[ItemDict]]) -> List[bool]: ...
def get_items_from_item_grid(player_id: str, key: str) -> List[Optional[ItemDict]]: ...
def update_item_grids(player_id: str, keys: Union[str, STuple]) -> bool: ...
def clear_items(player_id: str, item_pos_type: int, pos: int = 0) -> dict: ...
def get_item_pos(
    entity_id: str,
    pos_type: int,
    item_id: str,
    item_aux: int = -1,
    count: int = 1,
) -> List[int]: ...
def change_item_count(
    player_id: str,
    pos_type: int = ItemPosType.CARRIED,
    pos: int = 0,
    change: int = -1,
) -> None: ...
def deduct_inv_item(player_id: str, name: str, aux: int = -1, count: int = 1) -> bool: ...















