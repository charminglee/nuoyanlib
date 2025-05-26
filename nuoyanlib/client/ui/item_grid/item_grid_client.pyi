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
#   Last Modified : 2025-05-16
#
# ====================================================


from typing import List, Optional, Dict, Tuple
from mod.client.system.clientSystem import ClientSystem
from .._core._listener import lib_sys_event, ClientEventProxy
from .._core._typing import EventArgs
from .._core._utils import singleton


@singleton
class ItemGridClient(ClientEventProxy, ClientSystem):
    item_grid_path: Dict[str, Tuple[str, bool]]
    item_grid_size: Dict[str, int]
    item_grid_items: Dict[str, List[Optional[dict]]]
    registered_keys: Dict[str, List[str]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    @lib_sys_event
    def _UpdateItemGrids(self, args: EventArgs) -> None: ...
    def register_item_grid(self, key: str, ui_cls_path: str, path: str, size: int, is_single: bool) -> bool: ...
