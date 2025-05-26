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
#   Last Modified : 2025-05-17
#
# ====================================================


from typing import Tuple, List, Optional
from mod.common.minecraftEnum import ItemPosType as _ItemPosType


def deepcopy_item_dict(item_dict: Optional[dict]) -> Optional[dict]: ...
def gen_item_dict(
    newItemName: str,
    newAuxValue: str = 0,
    count: str = 1,
    showInHand: bool = True,
    enchantData: Optional[List[Tuple[int, int]]] = None,
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
