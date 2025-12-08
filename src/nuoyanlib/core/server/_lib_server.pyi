# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


from typing_extensions import Self
from typing import Dict, Optional, Callable, Union
from mod.server.system.serverSystem import ServerSystem
from .._types._typing import ArgsDict
from .._utils import singleton
from .._sys import NuoyanLibBaseSystem
from ..listener import ServerEventProxy, _lib_sys_event


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    query_cache: Dict[str, Dict[str, float]]
    callback_data: Dict[str, Dict[str, Union[Callable, int]]]
    def __init__(self: Self, namespace: str, system_name: str) -> None: ...
    @_lib_sys_event
    def _BroadcastToAllClient(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _NotifyToMultiClients(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _NotifyToClient(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...


def instance() -> Optional[NuoyanLibServerSystem]: ...
