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
#   Last Modified : 2025-01-26
#
# ====================================================


from typing import List, Optional, Dict, Tuple, Any
from mod.client.system.clientSystem import ClientSystem
from .._typing import EventArgs
from ._listener import event, lib_sys_event
from .._sys import NuoyanLibBaseSystem
from .._const import LIB_NAME, LIB_CLIENT_NAME, LIB_SERVER_NAME


class NuoyanLibClientSystem(NuoyanLibBaseSystem, ClientSystem):
    item_grid_path: Dict[str, Tuple[str, bool]]
    item_grid_size: Dict[str, int]
    item_grid_items: Dict[str, List[Optional[dict]]]
    registered_keys: Dict[str, List[str]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def broadcast_to_all_client(
        self: ...,
        event_name: str,
        event_data: Any,
        namespace: str = "",
        sys_name: str = "",
    ) -> None: ...
    def notify_to_multi_clients(
        self: ...,
        player_ids: List[str],
        event_name: str,
        event_data: Any,
        namespace: str = "",
        sys_name: str = "",
    ) -> None: ...
    @event("_NuoyanLibCall", LIB_NAME, LIB_CLIENT_NAME)
    @event("_NuoyanLibCall", LIB_NAME, LIB_SERVER_NAME)
    def _be_called(self: ..., args: EventArgs) -> None: ...
    @event("_NuoyanLibCallReturn", LIB_NAME, LIB_CLIENT_NAME)
    @event("_NuoyanLibCallReturn", LIB_NAME, LIB_SERVER_NAME)
    def _call_return(self: ..., args: EventArgs) -> None: ...
    @event("UiInitFinished")
    def _on_ui_init_finished(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("_SetQueryCache")
    def _on_set_query_cache(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("_SetQueryVar")
    def on_set_query_var(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("_UpdateItemGrids")
    def _on_update_item_grids(self: ..., args: EventArgs) -> None: ...
    def register_item_grid(self: ..., key: str, ui_cls_path: str, path: str, size: int, is_single: bool) -> bool: ...


_lib_sys: Optional[NuoyanLibClientSystem]


def get_lib_system() -> Optional[NuoyanLibClientSystem]: ...
