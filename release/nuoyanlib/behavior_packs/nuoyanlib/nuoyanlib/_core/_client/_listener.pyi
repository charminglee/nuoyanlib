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
#   Last Modified : 2024-06-16
#
# ====================================================


from types import InstanceType
from typing import List, Tuple, Callable, Union, Dict
from mod.client.system.clientSystem import ClientSystem


_ALL_CLIENT_ENGINE_EVENTS: Tuple[str, ...]
_ALL_CLIENT_LIB_EVENTS: Dict[str, str]
_lsn_func_args: List[Tuple[str, str, str, str, int]]


def event(
    event_name: Union[str, Callable] = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0,
) -> Callable: ...
def listen_custom(self: InstanceType) -> None: ...
def listen_engine_and_lib(self: ClientSystem) -> None: ...
def listen_for_lib_sys(name: str) -> Callable: ...
