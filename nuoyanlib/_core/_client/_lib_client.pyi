# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-13
|
| ==============================================
"""


from typing import List, Optional, Any, Dict, Callable, Union
from mod.client.system.clientSystem import ClientSystem
from .._types._typing import ArgsDict
from ..listener import ClientEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton


def instance() -> Optional[NuoyanLibClientSystem]: ...


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    __instance__: NuoyanLibClientSystem
    __inited__: bool
    __lib_flag__: int
    callback_data: Dict[str, Dict[str, Union[Callable, int]]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def broadcast_to_all_client(
        self,
        event_name: str,
        event_data: Any,
        ns: str = "",
        sys_name: str = "",
    ) -> None: ...
    def notify_to_multi_clients(
        self,
        player_ids: List[str],
        event_name: str,
        event_data: Any,
        ns: str = "",
        sys_name: str = "",
    ) -> None: ...
    def _SetQueryCache(self, args: ArgsDict) -> None: ...
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...
