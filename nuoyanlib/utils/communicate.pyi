# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from typing import Any, Callable, Union, List, Optional, Dict, Tuple, overload
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem


_CallbackType = Optional[Callable[[Dict[str, Any]], Any]]


class Caller(object):
    ns: str
    sys_name: str
    method: str
    def __init__(self, ns: str, sys_name: str, method: str = "") -> None: ...
    def __call__(
        self,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        method: str = "",
        player_id: Optional[Union[str, List[str]]] = None,
        callback: _CallbackType = None,
        delay_ret: float = -1,
    ) -> None: ...


def call_func(
    func_path: str,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    callback: _CallbackType = None,
    delay_ret: float = -1,
) -> None: ...
@overload
def broadcast_to_all_systems(
    event_name: str,
    event_args: Any,
    from_system: Union[ClientSystem, ServerSystem],
) -> None: ...
@overload
def broadcast_to_all_systems(
    event_name: str,
    event_args: Any,
    from_system: Tuple[str, str],
) -> None: ...
def call_callback(
    cb_or_uuid: Union[_CallbackType, str],
    delay_ret: float = -1,
    success: bool = Tuple,
    ret: Any = None,
    error: str = "",
    player_id: str = "",
) -> None: ...
def call_local(
    target_sys: Union[ClientSystem, ServerSystem],
    method: str,
    cb_or_uuid: Union[_CallbackType, str],
    delay_ret: float,
    args: Optional[Tuple[Any, ...]],
    kwargs: Optional[Dict[str, Any]],
) -> None: ...
def call(
    ns: str,
    sys_name: str,
    method: str,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    player_id: Optional[Union[str, List[str]]] = None,
    callback: _CallbackType = None,
    delay_ret: float = -1,
) -> None: ...
