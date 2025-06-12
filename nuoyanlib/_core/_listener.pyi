# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from typing import Callable, Optional, Tuple, Union, Any, List, Generator
from types import MethodType, FunctionType, InstanceType
from weakref import ReferenceType
from ._types._events import ClientEvent, ServerEvent
from ._types._typing import ArgsDict, PyBasicTypes


def _get_event_source(client: bool, event_name: str, ns: str = "", sys_name: str = "") -> Optional[Tuple[str, str]]: ...
def listen_for(ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...
def unlisten_for(ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...


class EventArgsProxy(dict):
    arg_dict: ArgsDict
    event_name: str
    def __init__(self: ..., arg_dict: ArgsDict, event_name: str) -> None: ...
    def __getattr__(self, key: str) -> PyBasicTypes: ...
    def __setattr__(self, key: str, value: PyBasicTypes) -> None: ...
    def __repr__(self) -> str: ...


class _BaseEventProxy(object):
    def __init__(self: ..., *args, **kwargs) -> None: ...
    def _listen_events(self) -> None: ...
    def _proxy_listen(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0,
    ) -> None: ...
class ClientEventProxy(ClientEvent, _BaseEventProxy): ...
class ServerEventProxy(ServerEvent, _BaseEventProxy): ...


class event(object):
    _ns: str
    _sys_name: str
    _priority: int
    _event_name: str
    _func: Callable
    __self__: Optional[ReferenceType[InstanceType]]
    _is_method: bool
    listen_args: List[Tuple[str, str, str, int]]
    def __init__(
        self: ...,
        event_name: Union[str, FunctionType, event] = "",
        ns: str = "",
        sys_name: str = "",
        priority: int = 0,
        is_method: bool = True,
    ) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Union[event, Any]: ...
    def __get__(self, ins: Any, cls: Any) -> event: ...
    def _bind_func(self, func: Union[FunctionType, event]) -> None: ...
    def _listen(self, args: Tuple[str, str, str, int]) -> None: ...
    @staticmethod
    def _get_all_event_ins(ins: InstanceType) -> Generator[event, None, None]: ...
    @staticmethod
    def listen_all(ins: Any) -> None: ...
    @staticmethod
    def unlisten_all(ins: Any) -> None: ...
    def unlisten(self) -> None: ...


def lib_sys_event(name: str) -> event: ...
