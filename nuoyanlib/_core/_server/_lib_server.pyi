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


from typing import Dict, Optional
from mod.server.system.serverSystem import ServerSystem
from .._types._typing import EventArgs
from .._listener import lib_sys_event, ServerEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton


def instance() -> Optional[NuoyanLibServerSystem]: ...


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    instance: NuoyanLibServerSystem
    query_cache: Dict[str, Dict[str, float]]
    @staticmethod
    def init() -> None: ...
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    @lib_sys_event
    def _ButtonCallbackTrigger(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _BroadcastToAllClient(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _NotifyToMultiClients(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _SetQueryVar(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _NuoyanLibCall(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _NuoyanLibCallReturn(self, args: EventArgs) -> None: ...
