# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Callable, Tuple, Union, Dict, Set, List
from types import MethodType
from ._types._events import ClientEvent, ServerEvent
from ._types._typing import ArgsDict, PyBasicTypes
from ._client._lib_client import NuoyanLibClientSystem
from ._server._lib_server import NuoyanLibServerSystem


ALL_CLIENT_ENGINE_EVENTS: Set[str]
ALL_CLIENT_LIB_EVENTS: Dict[str, str]
ALL_SERVER_ENGINE_EVENTS: Set[str]
ALL_SERVER_LIB_EVENTS: Dict[str, str]


class EventArgsProxy(object):
    arg_dict: ArgsDict
    def __init__(self: ..., arg_dict: ArgsDict) -> None: ...
    def __getattr__(self, key: str) -> PyBasicTypes: ...
    def __setattr__(self, key: str, value: PyBasicTypes) -> None: ...
    def __repr__(self) -> str: ...
    copy = dict.copy
    iterkeys = dict.iterkeys
    itervalues = dict.itervalues
    iteritems = dict.iteritems
    viewkeys = dict.viewkeys
    viewvalues = dict.viewvalues
    viewitems = dict.viewitems
    get = dict.get
    keys = dict.keys
    values = dict.values
    items = dict.items
    __len__ = dict.__len__
    __contains__ = dict.__contains__
    __getitem__ = dict.__getitem__
    __setitem__ = dict.__setitem__
    __cmp__ = dict.__cmp__
    __delitem__ = dict.__delitem__
    __eq__ = dict.__eq__
    __ge__ = dict.__ge__
    __gt__ = dict.__gt__
    __iter__ = dict.__iter__
    __le__ = dict.__le__
    __lt__ = dict.__lt__
    __ne__ = dict.__ne__


class BaseEventProxy(object):
    _lib_sys: Union[NuoyanLibClientSystem, NuoyanLibServerSystem]
    _engine_events: Set[str]
    _engine_ns: str
    _engine_sys: str
    _lib_events: Dict[str, str]
    def __init__(self: ..., *args, **kwargs) -> None: ...
    def _listen_events(self) -> None: ...
    def _parse_listen_args(self, method: MethodType) -> Tuple[int, List[List[str, str, str, int]]]: ...
    def _listen_proxy(
        self,
        namespace: str,
        system_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
    def _listen(
        self,
        namespace: str,
        system_name: str,
        event_name: str,
        method: MethodType,
        priority: int = 0
    ) -> None: ...
class ClientEventProxy(ClientEvent, BaseEventProxy): ...
class ServerEventProxy(ServerEvent, BaseEventProxy): ...


def event(
    event_name: Union[str, Callable] = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0,
) -> Callable: ...
def lib_sys_event(name: str) -> Callable: ...
