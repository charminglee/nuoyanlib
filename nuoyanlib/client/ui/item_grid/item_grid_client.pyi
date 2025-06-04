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


from typing import List, Optional, Dict, Tuple
from mod.client.system.clientSystem import ClientSystem
from ...._core._listener import lib_sys_event, ClientEventProxy
from ...._core._types._typing import ArgsDict
from ...._core._utils import singleton


@singleton
class ItemGridClient(ClientEventProxy, ClientSystem):
    item_grid_path: Dict[str, Tuple[str, bool]]
    item_grid_size: Dict[str, int]
    item_grid_items: Dict[str, List[Optional[dict]]]
    registered_keys: Dict[str, List[str]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    @lib_sys_event
    def _UpdateItemGrids(self, args: ArgsDict) -> None: ...
    def register_item_grid(self, key: str, ui_cls_path: str, path: str, size: int, is_single: bool) -> bool: ...
