# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-30
#
# ====================================================


from typing import Callable, Tuple, Union, Dict, Set, Optional, List
from types import MethodType
from ._types._listener import ClientEvent, ServerEvent
from ._client._lib_client import NuoyanLibClientSystem
from ._server._lib_server import NuoyanLibServerSystem


ALL_CLIENT_ENGINE_EVENTS: Set[str]
ALL_CLIENT_LIB_EVENTS: Dict[str, str]
ALL_SERVER_ENGINE_EVENTS: Set[str]
ALL_SERVER_LIB_EVENTS: Dict[str, str]


class BaseEventProxy(object):
    _lib_sys: Union[NuoyanLibClientSystem, NuoyanLibServerSystem]
    _engine_events: Set[str]
    _engine_ns: str
    _engine_sys: str
    _lib_events: Dict[str, str]
    def __init__(self: ..., *args, **kwargs) -> None: ...
    def _listen_events(self) -> None: ...
    def _parse_listen_args(self, method: MethodType) -> Tuple[int, List[List[str, str, str, int]]]: ...
    def _listen_proxy(
        self,
        namespace: str,
        system_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
    def _listen(
        self,
        namespace: str,
        system_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
class ClientEventProxy(ClientEvent, BaseEventProxy): ...
class ServerEventProxy(ServerEvent, BaseEventProxy): ...


def event(
    event_name: Union[str, Callable] = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0,
) -> Callable: ...
def lib_sys_event(name: str) -> Callable: ...
