# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  ================================================


from typing import Type, List, Optional, Dict, Callable, Any, Union
from collections import defaultdict
from types import MethodType
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem
from ..core._types._event_typing import ClientEvent, ServerEvent
from ..common.communicate import SyncData


class NySystem(object):
    def __init__(self) -> None: ...


class __NyClientSystem(ClientEvent, NySystem, ClientSystem):
    def __init__(self, namespace: str, system_name: str) -> None: ...


class __NyServerSystem(ServerEvent, NySystem, ServerSystem):
    def __init__(self, namespace: str, system_name: str) -> None: ...


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
