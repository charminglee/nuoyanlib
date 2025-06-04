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


from types import MethodType
from typing import Union, Dict, Tuple, Callable, Any, Literal
from mod.client import extraClientApi
from mod.server import extraServerApi
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from ._client._lib_client import NuoyanLibClientSystem
from ._server._lib_server import NuoyanLibServerSystem


def check_env(target: Literal["client", "server"]) -> None: ...
def get_lib_system() -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem, None]: ...
def is_apollo() -> bool: ...
def is_client() -> bool: ...
def get_api() -> Union[extraClientApi, extraServerApi]: ...
def get_comp_factory() -> Union[EngineCompFactoryClient, EngineCompFactoryServer]: ...


LEVEL_ID: str


class NuoyanLibBaseSystem(object):
    cond_func: Dict[int, Tuple[Callable[[], bool], Callable[[bool], Any], int]]
    cond_state: Dict[int, bool]
    __tick: int
    def __init__(self: ..., *args, **kwargs) -> None: ...
    def Update(self) -> None: ...
    def add_event_callback(self, event: str, callback: MethodType) -> None: ...
    def remove_event_callback(self, event: str, callback: MethodType) -> None: ...
    def add_condition_to_func(
        self,
        cond: Callable[[], bool],
        func: Callable[[bool], Any],
        freq: int,
    ) -> int: ...
    def remove_condition_to_func(self, cond_id: int) -> bool: ...
