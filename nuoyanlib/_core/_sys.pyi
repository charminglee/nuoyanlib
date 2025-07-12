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


from types import MethodType
from typing import Union, Dict, Tuple, Callable, Any, Literal, List, TypeVar, Type
from mod.client import extraClientApi
from mod.server import extraServerApi
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from ._client._lib_client import NuoyanLibClientSystem
from ._server._lib_server import NuoyanLibServerSystem


_T = TypeVar("_T")


def check_env(target: Literal["client", "server"]) -> None: ...
def get_lib_system() -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem, None]: ...
def is_apollo() -> bool: ...
def is_client() -> bool: ...
def get_api() -> Union[extraClientApi, extraServerApi]: ...
def get_comp_factory() -> Union[EngineCompFactoryClient, EngineCompFactoryServer]: ...


LEVEL_ID: str


class NuoyanLibBaseSystem(object):
    __tick: int
    cond_func: Dict[int, Tuple[Callable[[], bool], Callable[[bool], Any], int]]
    cond_state: Dict[int, bool]
    event_pool: Dict[str, List[Callable[[dict], Any]]]
    def __init__(self: ..., *args, **kwargs) -> None: ...
    @classmethod
    def register(cls: Type[_T]) -> _T: ...
    def get_lib_dict(self) -> Dict[str, Any]: ...
    def Update(self) -> None: ...
    def Destroy(self) -> None: ...
    def native_listen(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
    def native_unlisten(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
    def add_condition_to_func(self, cond: Callable[[], bool], func: Callable[[bool], Any], freq: int) -> int: ...
    def rm_condition_to_func(self, cond_id: int) -> bool: ...
