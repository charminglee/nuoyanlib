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
#   Last Modified : 2024-07-06
#
# ====================================================


from typing import List, Tuple, Callable, Union, Dict, Any
from ...server.server_system import NuoyanServerSystem


_ALL_SERVER_ENGINE_EVENTS: Tuple[str, ...]
_ALL_SERVER_LIB_EVENTS: Dict[str, str]
_lsn_func_args: List[Tuple[str, str, str, Callable, int]]
_SERVER_ENGINE_NAMESPACE: str
_SERVER_ENGINE_SYSTEM_NAME: str


def event(
    event_name: Union[str, Callable] = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0,
) -> Callable: ...
def listen_custom(self: Any) -> None: ...
def listen_engine_and_lib(self: NuoyanServerSystem) -> None: ...
def lib_sys_event(name: str) -> Callable: ...
