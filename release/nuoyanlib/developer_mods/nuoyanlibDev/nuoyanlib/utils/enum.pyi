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
#   Last Modified : 2023-11-26
#
# ====================================================


from typing import Dict, List, Tuple, Any, Optional


def search_data(data: Any, lst: list) -> bool: ...


ENTITY_LIST: List[Optional[Tuple[int, str, str, int]]]
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
