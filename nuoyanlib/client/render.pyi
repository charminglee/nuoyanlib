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


from typing import Tuple


def set_query_mod_var(entity_id: str, name: str, value: float, sync: bool = True) -> bool: ...
def add_player_render_resources(player_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
def add_entity_render_resources(entity_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
