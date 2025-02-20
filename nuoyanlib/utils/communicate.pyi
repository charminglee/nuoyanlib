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
#   Last Modified : 2025-02-16
#
# ====================================================


from  typing import Any, Callable, Union, List, Optional, Dict, Tuple
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem


__CallbackType = Optional[Callable[[Dict[str, Any]], Any]]


class Caller(object):
    namespace: str
    system_name: str
    method: str
    def __init__(self, namespace: str, system_name: str, method: str = "") -> None: ...
    def __call__(
        self,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        method: str = "",
        player_id: Optional[Union[str, List[str]]] = None,
        callback: __CallbackType = None,
        delay_ret: float = -1,
    ) -> None: ...


def call_func(
    func_path: str,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    callback: __CallbackType = None,
    delay_ret: float = -1,
) -> None: ...
def broadcast_to_all_systems(
    event_name: str,
    event_args: Any,
    from_system: Union[ClientSystem, ServerSystem, Tuple[str, str]],
) -> None: ...


__callback_data: Dict[str, Dict[str, Union[int, __CallbackType]]]


def call_callback(
    cb_or_uuid: Union[__CallbackType, str],
    delay_ret: float = -1,
    success: bool = Tuple,
    ret: Any = None,
    error: str = "",
    player_id: str = "",
) -> None: ...
def call_local(
    target_sys: Union[ClientSystem, ServerSystem],
    method: str,
    cb_or_uuid: Union[__CallbackType, str],
    delay_ret: float,
    args: Optional[Tuple[Any, ...]],
    kwargs: Optional[Dict[str, Any]],
) -> None: ...
def __notify_call(
    namespace: str,
    system_name: str,
    method: str,
    player_id: Union[str, List[str], None],
    callback: __CallbackType,
    delay_ret: float,
    args: Optional[Tuple[Any, ...]],
    kwargs: Optional[Dict[str, Any]],
) -> None: ...
def call(
    namespace: str,
    system_name: str,
    method: str,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    player_id: Optional[Union[str, List[str]]] = None,
    callback: __CallbackType = None,
    delay_ret: float = -1,
) -> None: ...
