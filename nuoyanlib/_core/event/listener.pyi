# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-25
|
| ==============================================
"""


from typing import Callable, Optional, Tuple, Generator, List, Any, DefaultDict, Set, Union
from types import MethodType
from ._events import ClientEvent, ServerEvent
from .._types._typing import ArgsDict, PyBasicTypes, STuple


class _EventPool(object):
    __slots__: STuple
    pool: DefaultDict[int, Set[Callable]]
    priorities: List[int]
    lock: bool
    remove_lst: List[Tuple[Callable, int]]
    add_lst: List[Tuple[Callable, int]]
    __name__: str
    def __init__(self: ...) -> None: ...
    def __nonzero__(self) -> bool: ...
    def __call__(self, args: Optional[dict] = None) -> None: ...
    def add(self, func: Callable, priority: int = 0) -> None: ...
    def remove(self, func: Callable, priority: int = 0) -> None: ...
    @classmethod
    def get(cls, ns: str, sys_name: str, event_name: str) -> _EventPool: ...
    @classmethod
    def listen_for(cls, ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...
    @classmethod
    def unlisten_for(cls, ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> None: ...
    @classmethod
    def has_listened(cls, ns: str, sys_name: str, event_name: str, func: Callable, priority: int = 0) -> bool: ...


class EventArgsProxy(object):
    __slots__: STuple
    _arg_dict: ArgsDict
    _event_name: str
    def __init__(self: ..., arg_dict: ArgsDict, event_name: str) -> None: ...
    def __getattr__(self, key: str) -> PyBasicTypes: ...
    def __setattr__(self, key: str, value: PyBasicTypes) -> None: ...
    def __repr__(self) -> str: ...
    get = dict.get
    keys = dict.keys
    values = dict.values
    items = dict.items
    has_key = dict.has_key # NOQA
    copy = dict.copy
    iterkeys = dict.iterkeys
    itervalues = dict.itervalues
    iteritems = dict.iteritems
    viewkeys = dict.viewkeys
    viewvalues = dict.viewvalues
    viewitems = dict.viewitems
    __len__ = dict.__len__
    __contains__ = dict.__contains__
    __getitem__ = dict.__getitem__
    __setitem__ = dict.__setitem__
    __cmp__ = dict.__cmp__
    __eq__ = dict.__eq__
    __ge__ = dict.__ge__
    __gt__ = dict.__gt__
    __iter__ = dict.__iter__
    __le__ = dict.__le__
    __lt__ = dict.__lt__
    __ne__ = dict.__ne__


def _get_event_source(in_client: bool, event_name: str, ns: str = "", sys_name: str = "") -> Optional[Tuple[str, str]]: ...
def _parse_event_args(func: Callable, event_name: str, ns: str, sys_name: str) -> Tuple[str, str, str]: ...


class _BaseEventProxy(object):
    _is_client: bool
    def __init__(self: ..., *args, **kwargs) -> None: ...
    def _process_engine_events(self) -> None: ...
    def _create_proxy(
        self,
        ns: str,
        sys_name: str,
        event_name: str,
        method: MethodType,
    ) -> None: ...
class ClientEventProxy(ClientEvent, _BaseEventProxy): ...
class ServerEventProxy(ServerEvent, _BaseEventProxy): ...


def event(
    event_name: Union[str, Callable] = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    is_method: bool = True,
) -> Callable: ...
def _get_event_args(func: Callable) -> List[Tuple[str, str, str, int]]: ...
def listen_event(
    func: Callable,
    event_name: str = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    use_decorator: bool = False,
) -> None: ...
def unlisten_event(
    func: Callable,
    event_name: str = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    use_decorator: bool = False,
) -> None: ...
def _get_all_event_args(ins: Any) -> Generator[Tuple[MethodType, List[Tuple[str, str, str, int]]], None, None]: ...
def listen_all_events(ins: Any) -> None: ...
def unlisten_all_events(ins: Any) -> None: ...
def has_listened(
    func: Callable,
    event_name: str = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
) -> bool: ...
def lib_sys_event(name: str) -> Callable: ...
