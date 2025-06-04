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


from typing import List, Optional, Any
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from .._types._typing import ArgsDict
from .._listener import event, lib_sys_event, ClientEventProxy
from .._sys import NuoyanLibBaseSystem
from .._const import LIB_NAME, LIB_CLIENT_NAME, LIB_SERVER_NAME
from .._utils import singleton


def instance() -> Optional[NuoyanLibClientSystem]: ...


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    instance: NuoyanLibClientSystem
    @staticmethod
    def register() -> None: ...
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
    def _SetQueryCache(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    @event(namespace=LIB_NAME, system_name=LIB_CLIENT_NAME)
    @event(namespace=LIB_NAME, system_name=LIB_SERVER_NAME)
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    @event(namespace=LIB_NAME, system_name=LIB_CLIENT_NAME)
    @event(namespace=LIB_NAME, system_name=LIB_SERVER_NAME)
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...
