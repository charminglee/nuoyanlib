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


from typing import ClassVar, Callable, Optional, Tuple, Generator, List, Any, Dict, Set, overload
from types import MethodType
from ._types._event_typing import ClientEvent, ServerEvent
from ._types._typing import Self, ArgsDict, PyBasicTypes, STuple, F


ALL_CLIENT_LIB_EVENTS: Dict[str, str]
ALL_SERVER_LIB_EVENTS: Dict[str, str]


class _EventPool(object):
    __slots__: ClassVar[STuple]
    pool: Dict[int, Set[Callable]]
    priorities: List[int]
    lock: bool
    remove_lst: List[Tuple[Callable, int]]
    add_lst: List[Tuple[Callable, int]]
    __name__: str
    def __init__(self: Self, event_id: str) -> None: ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __call__(self, args: Optional[dict] = None) -> None: ...
    def _add(self, func: Callable, priority: int = 0) -> None: ...
    def _remove(self, func: Callable, priority: int = 0) -> None: ...
    @staticmethod
    def _get(event_name: str, ns: str, sys_name: str, new: bool = True) -> Optional[_EventPool]: ...
    @staticmethod
    def listen_event(func: Callable, event_name: str, ns: str, sys_name: str, priority: int = 0) -> None: ...
    @staticmethod
    def unlisten_event(func: Callable, event_name: str, ns: str, sys_name: str, priority: int = 0) -> None: ...
    @staticmethod
    def is_listened(func: Callable, event_name: str, ns: str, sys_name: str, priority: int = 0) -> bool: ...


def _get_event_source(is_client: bool, event_name: str) -> Optional[Tuple[str, str]]: ...
def _parse_listen_args(func: Callable, event_name: str, ns: str, sys_name: str) -> Tuple[str, str, str]: ...
@overload
def event(
    event_name: str = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    is_method: bool = True,
) -> Callable[[F], F]: ...
@overload
def event(
    event_name: F,
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
    is_method: bool = True,
) -> F: ...
def _get_listen_args(func: Callable) -> Optional[List[Tuple[str, str, str, int]]]: ...
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
def _iter_all_events(ins: Any) -> Generator[Tuple[MethodType, List[Tuple[str, str, str, int]]]]: ...
def listen_all_events(ins: Any) -> None: ...
def unlisten_all_events(ins: Any) -> None: ...
def is_listened(
    func: Callable,
    event_name: str = "",
    ns: str = "",
    sys_name: str = "",
    priority: int = 0,
) -> bool: ...


class EventArgsWrap(object):
    __slots__: ClassVar[STuple]
    _arg_dict: ArgsDict
    _event_name: str
    def __init__(self: Self, arg_dict: ArgsDict, event_name: str) -> None: ...
    def __getattr__(self, key: str) -> PyBasicTypes: ...
    def __setattr__(self, key: str, value: PyBasicTypes) -> None: ...
    def __repr__(self) -> str: ...
    __iter__ = dict.__iter__
    __eq__ = dict.__eq__
    __ne__ = dict.__ne__
    __len__ = dict.__len__
    __contains__ = dict.__contains__
    keys = dict.keys
    values = dict.values
    items = dict.items
    iterkeys = dict.iterkeys
    itervalues = dict.itervalues
    iteritems = dict.iteritems
    get = dict.get
    copy = dict.copy


class BaseEventProxy(object):
    def __init__(self: Self, *args, **kwargs) -> None: ...
    def _create_proxy(
        self,
        method: MethodType,
        event_name: str,
        ns: str,
        sys_name: str,
    ) -> None: ...
class ClientEventProxy(ClientEvent, BaseEventProxy): ...
class ServerEventProxy(ServerEvent, BaseEventProxy): ...


def _lib_sys_event(name: str = "", from_client: Optional[bool] = None) -> Callable: ...
