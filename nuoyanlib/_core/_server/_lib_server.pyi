# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from typing import Dict, Optional
from mod.server.system.serverSystem import ServerSystem
from .._types._typing import ArgsDict
from .._listener import lib_sys_event, ServerEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton


def instance() -> Optional[NuoyanLibServerSystem]: ...


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    instance: NuoyanLibServerSystem
    query_cache: Dict[str, Dict[str, float]]
    @staticmethod
    def register() -> None: ...
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    @lib_sys_event
    def _ButtonCallbackTrigger(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _BroadcastToAllClient(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _NotifyToMultiClients(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...
