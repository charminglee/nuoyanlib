# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-17
|
| ==============================================
"""


from typing import Callable, Optional, Tuple, Union, Generator, List
from types import MethodType, FunctionType, InstanceType
from ._types._events import ClientEvent, ServerEvent
from ._types._typing import ArgsDict, PyBasicTypes


def _get_event_source(client: bool, event_name: str, ns: str = "", sys_name: str = "") -> Optional[Tuple[str, str]]: ...
def _listen_for(ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...
def _unlisten_for(ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...


class EventArgsProxy(dict):
    _arg_dict: ArgsDict
    _event_name: str
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


_LISTEN_ARGS_KEY: str


def event(
    event_name: Union[str, FunctionType] = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    is_method: bool = True,
) -> Callable: ...
def _get_event_args(func: FunctionType) -> List[Tuple[str, str, str, int]]: ...
def listen_event(func: FunctionType) -> None: ...
def unlisten_event(func: FunctionType) -> None: ...
def _get_all_event_args(ins: InstanceType) -> Generator[Tuple[MethodType, List[Tuple[str, str, str, int]]], None, None]: ...
def listen_all_events(ins: InstanceType) -> None: ...
def unlisten_all_events(ins: InstanceType) -> None: ...
def lib_sys_event(name: str) -> Callable: ...
