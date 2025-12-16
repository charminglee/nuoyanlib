# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from typing import Any, Callable, Union, List, Optional, Dict, Tuple
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem
from ..core._types._typing import Self


__CallbackType = Union[Callable[[bool, Any], Any], Callable[[bool, Any, str], Any], None]


class Caller(object):
    ns: str
    sys_name: str
    method: str
    def __init__(self: Self, ns: str, sys_name: str, method: str = "") -> None: ...
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
    from_system: Union[ClientSystem, ServerSystem],
) -> None: ...
def _call_callback(
    cb_or_uuid: Union[__CallbackType, str],
    delay_ret: float,
    cb_args: Tuple[bool, Any, str],
) -> None: ...
def _call_local(
    ns: str,
    sys_name: str,
    method: str,
    cb_or_uuid: Union[__CallbackType, str],
    delay_ret: float,
    args: Optional[Tuple[Any, ...]],
    kwargs: Optional[Dict[str, Any]],
) -> None: ...
def _call_remote(
    ns: str,
    sys_name: str,
    method: str,
    player_id: Optional[List[str]],
    callback: Callable,
    delay_ret: float,
    args: Any,
    kwargs: Any,
) -> None: ...
def call(
    ns: str,
    sys_name: str,
    method: str,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    player_id: Optional[Union[str, List[str]]] = None,
    callback: __CallbackType = None,
    delay_ret: float = -1,
) -> None: ...
