# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-18
|
| ==============================================
"""


from typing import List, Optional, Any, Dict, Callable, Union, TypedDict, Tuple
from mod.client.system.clientSystem import ClientSystem
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from .._types._typing import ArgsDict, FTuple3
from ..listener import ClientEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton
from ...utils.time_ease import TimeEase


class __GROUND_SHATTER_DATA(TypedDict):
    inited: bool
    attr_comp: ModAttrComponentClient
    render_comp: ActorRenderCompClient
    te: TimeEase
    geo_name: str
    pos: FTuple3
    time: float
    tilt_angle: float
    min_height: float
    max_height: float
    in_time: float
    out_time: float
    in_dist: float
    out_dist: float
    block: Tuple[str, int]


def instance() -> Optional[NuoyanLibClientSystem]: ...


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    __instance__: NuoyanLibClientSystem
    __inited__: bool
    __lib_flag__: int
    callback_data: Dict[str, Dict[str, Union[Callable, int]]]
    _ground_shatter_data: Dict[str, __GROUND_SHATTER_DATA]
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
    def _init_ground_shatter_effect(self, data: __GROUND_SHATTER_DATA) -> None: ...
    def _update_ground_shatter_effect(self) -> None: ...
