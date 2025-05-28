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
#   Last Modified : 2025-05-28
#
# ====================================================


from typing import List, Optional, Any
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from .._typing import EventArgs
from .._listener import event, lib_sys_event, ClientEventProxy
from .._sys import NuoyanLibBaseSystem
from .._const import LIB_NAME, LIB_CLIENT_NAME, LIB_SERVER_NAME


def instance() -> Optional[NuoyanLibClientSystem]: ...


class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    instance: NuoyanLibClientSystem
    @staticmethod
    def init() -> None: ...
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def broadcast_to_all_client(
        self,
        event_name: str,
        event_data: Any,
        namespace: str = "",
        sys_name: str = "",
    ) -> None: ...
    def notify_to_multi_clients(
        self,
        player_ids: List[str],
        event_name: str,
        event_data: Any,
        namespace: str = "",
        sys_name: str = "",
    ) -> None: ...
    def register_and_create_ui(
        self,
        namespace: str,
        ui_key: str,
        cls_path: str,
        ui_screen_def: str,
        stack: bool = False,
        param: Optional[dict] = None,
    ) -> Optional[ScreenNode]: ...
    @lib_sys_event
    def _SetQueryCache(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _SetQueryVar(self, args: EventArgs) -> None: ...
    @event(namespace=LIB_NAME, system_name=LIB_CLIENT_NAME)
    @event(namespace=LIB_NAME, system_name=LIB_SERVER_NAME)
    def _NuoyanLibCall(self, args: EventArgs) -> None: ...
    @event(namespace=LIB_NAME, system_name=LIB_CLIENT_NAME)
    @event(namespace=LIB_NAME, system_name=LIB_SERVER_NAME)
    def _NuoyanLibCallReturn(self, args: EventArgs) -> None: ...
