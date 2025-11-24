# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from typing import Dict, Any, Optional, Callable, Union, TypedDict, List
from ..core._types._typing import ArgsDict, STuple
from ..core.listener import event, ServerEventProxy


__DataType = Union[str, int, float, bool, list, dict, None]
class __DataDict(TypedDict):
    key: str
    value: __DataType
__SimpleDataDict = Dict[str, __DataType]
class __Entity(TypedDict):
    data: List[__DataDict]
class __CallbackDict(TypedDict):
    code: int
    message: str
    entity: __Entity
class __SimpleCallbackDict(TypedDict):
    code: int
    message: str
    data: __SimpleDataDict
__Callback = Callable[[Optional[__SimpleCallbackDict]], Any]
class __OrderDict(TypedDict):
    order_id: int
    timestamp: int
    cmd: str
    product_count: int
class __SimpleOrderDict(TypedDict):
    timestamp: int
    cmd: str
    product_count: int
class __OrderEntity(TypedDict):
    orders: List[__OrderDict]
class __OrderCallbackDict(TypedDict):
    entity: __OrderEntity
__SimpleOrderCallbackDict = Dict[int, __SimpleOrderDict]
__OrderCallback = Callable[[Optional[__SimpleOrderCallbackDict]], Any]


_IS_LOBBY: bool
_UID_DATA_KEY: str
_GLOBAL_DATA_KEY: str


class LobbyDataMgr(ServerEventProxy):
    _default: Dict[str, Callable[[], __DataType]]
    _uid: Dict[str, int]
    global_data: __SimpleDataDict
    """
    全局数据字典。
    """
    uid_data: Dict[str, Dict[int, __DataType]]
    """
    玩家数据字典。
    """
    def __init__(self: ...) -> None: ...
    @event("UiInitFinished")
    def _on_player_join(self, args: ArgsDict) -> None: ...
    def _to_uid(self, player_id: str) -> int: ...
    def register(self, key: str, default: Callable[[], __DataType] = None, is_global: bool = False) -> None: ...
    def _simplify_response(self, response: Union[__CallbackDict, __OrderCallbackDict]) -> None: ...
    def _set_default(self, response: __SimpleCallbackDict, keys: STuple) -> None: ...
    def _update_cache(self, uid: int, data: __SimpleDataDict) -> None: ...
    def fetch(
        self,
        player: Union[int, str] = 0,
        *keys: str,
        callback: Optional[__Callback] = None,
        simulate: Optional[__SimpleCallbackDict] = None,
    ) -> None: ...
    def _set(
        self,
        callback: __Callback,
        uid: int,
        order_id: Optional[int],
        getter: Callable[[], List[__DataDict]],
    ) -> None: ...
    def update(
        self,
        key: str,
        exp: Callable[[__DataType], __DataType],
        player: Union[int, str] = 0,
        *,
        order_id: Optional[int] = None,
        callback: Optional[__Callback] = None,
    ) -> None: ...
    def set(
        self,
        key: str,
        value: __DataType,
        player: Union[int, str] = 0,
        *,
        order_id: Optional[int] = None,
        callback: Optional[__Callback] = None,
    ) -> None: ...
    def get(self, key: str, player: Union[int, str] = 0) -> __DataType: ...
    def ship(
        self,
        order_id: int,
        player: Union[int, str],
        *,
        callback: Optional[__Callback] = None,
    ) -> None: ...
    def query(
        self,
        player: Union[int, str] = 0,
        *,
        callback: Optional[__OrderCallback] = None,
        simulate: Optional[__SimpleOrderCallbackDict] = None,
    ) -> None: ...
