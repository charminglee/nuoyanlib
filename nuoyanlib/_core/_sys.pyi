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
#   Last Modified : 2025-05-28
#
# ====================================================


from types import MethodType
from typing import Union, Dict, Tuple, Callable, Any, Literal
import mod.client.extraClientApi as client_api
import mod.server.extraServerApi as server_api
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from ._client._lib_client import NuoyanLibClientSystem
from ._server._lib_server import NuoyanLibServerSystem
from ._utils import singleton


def check_env(target: Literal["client", "server"]) -> None: ...
def get_lib_system() -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem, None]: ...
def is_apollo() -> bool: ...
def is_client() -> bool: ...
def get_api() -> Union[client_api, server_api]: ...
def get_comp_factory() -> Union[EngineCompFactoryClient, EngineCompFactoryServer]: ...


LEVEL_ID: str


@singleton
class NuoyanLibBaseSystem(object):
    instance: NuoyanLibBaseSystem
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
