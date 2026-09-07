# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


import sys
from typing import Type, List, Optional, Dict, Callable, Any, Union, Tuple
from collections import defaultdict
from types import MethodType
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem
from ..core._types._event_typing import ClientEvent, ServerEvent
from ..core._types._typing import T
from ..common.communicate import SyncData


class NySystemMeta(type):
    def __new__(metacls: Type[T], cls_name: str, bases: Tuple[type, ...], cls_dict: Dict[str, Any]) -> T: ...


if sys.version_info <= (2, 7):
    class __NyClientSystem(ClientEvent, ClientSystem):
        __metaclass__ = NySystemMeta
    class __NyServerSystem(ServerEvent, ServerSystem):
        __metaclass__ = NySystemMeta
else:
    class __NyClientSystem(ClientEvent, ClientSystem, metaclass=NySystemMeta): ...
    class __NyServerSystem(ServerEvent, ServerSystem, metaclass=NySystemMeta): ...


def _get_ncs_cls() -> Type[__NyClientSystem]: ...
def _get_nss_cls() -> Type[__NyServerSystem]: ...


class NuoyanLibBaseSystem(object):
    all_sd: defaultdict[str, List[SyncData]]
    unregister_sd_data: Dict[str, Any]
    is_client: bool
    def __init__(self) -> None: ...
    @classmethod
    def run(cls) -> bool: ...
    def Destroy(self) -> None: ...
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
    def _NuoyanLibSyncData(self, all_data: Dict[str, Any]) -> None: ...
    def register_sd(self, sd: SyncData) -> None: ...
    def sync(self, key: str) -> None: ...
    def sync_all(self, player_id: Optional[str] = None) -> None: ...
