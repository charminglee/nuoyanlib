# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


from typing import Tuple


def set_query_mod_var(entity_id: str, name: str, value: float, sync: bool = True) -> None: ...
def add_player_render_resources(player_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
def add_entity_render_resources(entity_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
