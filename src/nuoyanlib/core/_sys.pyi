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


from types import MethodType
from typing import Optional, Union, Dict, Tuple, Callable, Any, Literal, List, Type
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from .client._lib_client import NuoyanLibClientSystem
from .server._lib_server import NuoyanLibServerSystem
from .client.comp import CF as CCF
from .server.comp import CF as SCF
from ._types._typing import Self


def load_extensions() -> None: ...
def get_env() -> Literal["client", "server"]: ...
def check_env(target: Literal["client", "server"]) -> None: ...
def get_lib_system(_is_client: Optional[bool] = None) -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem, None]: ...
def is_apollo() -> bool: ...
def is_client() -> bool: ...
def get_api(_is_client: Optional[bool] = None) -> Union[Type[c_api], Type[s_api]]: ...
def get_comp_factory(_is_client: Optional[bool] = None) -> Union[EngineCompFactoryClient, EngineCompFactoryServer]: ...
def get_lv_comp(_is_client: Optional[bool] = None) -> Union[CCF, SCF]: ...
def get_cf(entity_id: str, _is_client: Optional[bool] = None) -> Union[CCF, SCF]: ...


LEVEL_ID: str


class NuoyanLibBaseSystem(object):
    __tick: int
    cond_func: Dict[int, Tuple[Callable[[], bool], Callable[[bool], Any], int]]
    cond_state: Dict[int, bool]
    event_pool: Dict[str, List[Callable[[dict], Any]]]
    def __init__(self: Self, *args, **kwargs) -> None: ...
    @classmethod
    def register(cls) -> bool: ...
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
