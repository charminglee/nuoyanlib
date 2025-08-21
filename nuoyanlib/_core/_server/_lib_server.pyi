# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-21
|
| ==============================================
"""


from typing import Dict, Optional, Callable, Union
from mod.server.system.serverSystem import ServerSystem
from .._types._typing import ArgsDict
from ..event.listener import ServerEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton


def instance() -> Optional[NuoyanLibServerSystem]: ...


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    __instance__: NuoyanLibServerSystem
    __inited__: bool
    __lib_flag__: int
    query_cache: Dict[str, Dict[str, float]]
    callback_data: Dict[str, Dict[str, Union[Callable, int]]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def _ButtonCallbackTrigger(self, args: ArgsDict) -> None: ...
    def _BroadcastToAllClient(self, args: ArgsDict) -> None: ...
    def _NotifyToMultiClients(self, args: ArgsDict) -> None: ...
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...
