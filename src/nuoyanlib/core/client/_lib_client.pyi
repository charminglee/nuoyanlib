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


from typing import List, Optional, Any, Dict, Callable, Union, TypedDict, Tuple
from mod.client.system.clientSystem import ClientSystem
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from .._types._typing import Self, ArgsDict, FTuple3
from .._const import LIB_NAME, LIB_CLIENT_NAME
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton
from ..listener import ClientEventProxy, _lib_sys_event
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


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    callback_data: Dict[str, Dict[str, Union[Callable, int]]]
    _ground_shatter_data: Dict[str, __GROUND_SHATTER_DATA]
    def __init__(self: Self, namespace: str, system_name: str) -> None: ...
    def broadcast_to_all_client(
        self,
        event_name: str,
        event_data: Any,
        ns: str = LIB_NAME,
        sys_name: str = LIB_CLIENT_NAME,
    ) -> None: ...
    def notify_to_multi_clients(
        self,
        player_ids: List[str],
        event_name: str,
        event_data: Any,
        ns: str = LIB_NAME,
        sys_name: str = LIB_CLIENT_NAME,
    ) -> None: ...
    def notify_to_client(
        self,
        player_id: str,
        event_name: str,
        event_data: Any,
        ns: str = LIB_NAME,
        sys_name: str = LIB_CLIENT_NAME,
    ) -> None: ...
    @_lib_sys_event
    def _SetQueryCache(self, args: ArgsDict) -> None: ...
    @_lib_sys_event
    def _SetQueryVar(self, args: ArgsDict) -> None: ...
    @_lib_sys_event(from_client=True)
    @_lib_sys_event(from_client=False)
    def _NuoyanLibCall(self, args: ArgsDict) -> None: ...
    @_lib_sys_event(from_client=True)
    @_lib_sys_event(from_client=False)
    def _NuoyanLibCallReturn(self, args: ArgsDict) -> None: ...
    def _init_ground_shatter_effect(self, data: __GROUND_SHATTER_DATA) -> None: ...
    def _update_ground_shatter_effect(self) -> None: ...
    @_lib_sys_event
    def _NuoyanLibVisualizeArea(self, args: ArgsDict) -> None: ...


def instance() -> Optional[NuoyanLibClientSystem]: ...
