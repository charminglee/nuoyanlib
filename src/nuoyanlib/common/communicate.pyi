# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-12
#  ⠀
# =================================================


from typing import Any, Callable, ClassVar, Literal, Union, List, Optional, Dict, Tuple, Generic
from mod.client.system.clientSystem import ClientSystem
from mod.server.system.serverSystem import ServerSystem
from ..core._types._typing import Self, SlotsType, T


__CallbackType = Union[Callable[[bool, Any], Any], Callable[[bool, Any, str], Any], None]


class SyncData(Generic[T]):
    __slots__: SlotsType
    F_SOURCE: ClassVar[Literal[-1]]
    F_FROM_CLIENT: ClassVar[Literal[0]]
    F_FROM_SERVER: ClassVar[Literal[1]]
    key: str
    value: Union[T, Any]
    _flag: int
    _on_sync: Union[
        Callable[[str, str, Union[T, Any], Union[T, Any]], Any],
        Callable[[str, Union[T, Any], Union[T, Any]], Any],
        None,
    ]
    _player_id: Optional[str]
    _is_dirty: bool
    def __init__(self: Self, key: str, default: Optional[T] = None) -> None: ...
    @classmethod
    def from_client(
        cls,
        player_id: str,
        key: str,
        default: Optional[T] = None,
        on_sync: Optional[Callable[[str, str, Union[T, Any], Union[T, Any]], Any]] = None,
    ) -> SyncData[T]: ...
    @classmethod
    def from_server(
        cls,
        key: str,
        default: Optional[T] = None,
        on_sync: Optional[Callable[[str, Union[T, Any], Union[T, Any]], Any]] = None,
    ) -> SyncData[T]: ...
    def __repr__(self) -> str: ...
    def set(self, value: Union[T, Any], sync: bool = False) -> None: ...
    def get(self) -> Union[T, Any]: ...
    def sync(self) -> None: ...
    @staticmethod
    def sync_all() -> None: ...
    def _on_engine_sync(self, new_value: Union[T, Any]) -> None: ...


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
