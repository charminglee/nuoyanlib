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
#   Last Modified : 2025-02-21
#
# ====================================================


from typing import Tuple, Callable, Union, Dict, TypeVar
from types import MethodType


_T = TypeVar("_T", bound=type)


__ALL_CLIENT_ENGINE_EVENTS: Tuple[str, ...]
__ALL_CLIENT_LIB_EVENTS: Dict[str, str]
__ALL_SERVER_ENGINE_EVENTS: Tuple[str, ...]
__ALL_SERVER_LIB_EVENTS: Dict[str, str]
__CLIENT_ENGINE_NAMESPACE = str
__CLIENT_ENGINE_SYSTEM_NAME = str
__SERVER_ENGINE_NAMESPACE = str
__SERVER_ENGINE_SYSTEM_NAME = str


def quick_listen(cls: _T) -> _T: ...
def event(
    event_name: Union[str, Callable] = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0,
) -> Callable: ...
def __listen(
    namespace: str,
    system_name: str,
    event_name: str,
    ins: object,
    method: MethodType,
    priority: int = 0,
) -> bool: ...
def __listen_custom(ins: object) -> None: ...
def __listen_engine_and_lib(ins: object) -> None: ...
def lib_sys_event(name: str) -> Callable: ...
