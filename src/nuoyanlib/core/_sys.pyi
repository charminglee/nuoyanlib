# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-12
#  ⠀
# =================================================


from collections import defaultdict
import threading
from types import MethodType
from typing import List, Optional, Union, Dict, Tuple, Callable, Any, Literal, Type
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from ._types._typing import Self
from .client._lib_client import NuoyanLibClientSystem
from .server._lib_server import NuoyanLibServerSystem
from .client.comp import CF as CCF
from .server.comp import CF as SCF
from ..utils.communicate import SyncData


def load_extensions() -> None: ...
def get_env() -> Literal["client", "server"]: ...
def check_env(target: Literal["client", "server"]) -> None: ...
_THREAD_LOCAL: threading.local
def get_lib_system() -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem]: ...
def is_client() -> bool: ...
def get_api() -> Union[Type[c_api], Type[s_api]]: ...
def get_lv_comp() -> Union[CCF, SCF]: ...
def get_cf(entity_id: str) -> Union[CCF, SCF]: ...
LEVEL_ID: str


class NuoyanLibBaseSystem(object):
    __tick: int
    cond_func: Dict[int, Tuple[Callable[[], bool], Callable[[bool], Any], int]]
    cond_state: Dict[int, bool]
    all_sd: defaultdict[str, List[SyncData]]
    unregister_sd_data: Dict[str, Any]
    is_client: bool
    def __init__(self: Self, *args, **kwargs) -> None: ...
    @classmethod
    def register(cls) -> bool: ...
    def Destroy(self) -> None: ...
    def Update(self) -> None: ...
    def native_listen(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: Union[MethodType, Callable[[Dict[str, Any]], Any]],
        priority: int = 0
    ) -> None: ...
    def native_unlisten(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: Union[MethodType, Callable[[Dict[str, Any]], Any]],
        priority: int = 0
    ) -> None: ...
    def add_condition_to_func(self, cond: Callable[[], bool], func: Callable[[bool], Any], freq: int) -> int: ...
    def rm_condition_to_func(self, cond_id: int) -> bool: ...
    def _NuoyanLibSyncData(self, all_data: Dict[str, Any]) -> None: ...
    def register_sd(self, sd: SyncData) -> None: ...
    def sync(self, key: str) -> None: ...
    def sync_all(self, player_id: Optional[str] = None) -> None: ...
