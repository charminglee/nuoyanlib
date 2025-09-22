# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-22
|
| ==============================================
"""


from typing import Callable, Any, Optional, overload, Hashable, Dict, TypeVar
from threading import Timer
from mod.common.utils.timer import CallLater


_F = TypeVar("_F", bound=Callable[[], Any])


_c_delay_timers: Dict[Hashable, CallLater]
_s_delay_timers: Dict[Hashable, CallLater]
_c_repeat_timers: Dict[Hashable, CallLater]
_s_repeat_timers: Dict[Hashable, CallLater]


def _set_timer(t: float, func: Callable[[], Any], is_repeat: bool, key: Optional[Hashable]) -> None: ...
@overload
def delay(t: float = 0, key: Optional[Hashable] = None) -> Callable[[_F], _F]: ...
@overload
def delay(t: _F) -> _F: ...
@overload
def repeat(t: float = 0, key: Optional[Hashable] = None) -> Callable[[_F], _F]: ...
@overload
def repeat(t: _F) -> _F: ...


class McTimer(object):
    type: str
    sec: float
    func: Optional[Callable]
    args: Any
    kwargs: Any
    _pause: bool
    _cancel: bool
    __timer: Optional[Timer]
    def __init__(self: ..., ttype: str, sec: float, func: Callable, *args: Any, **kwargs: Any): ...
    def _execute(self) -> Any: ...
    def __func(self) -> None: ...
    def Start(self) -> McTimer: ...
    def Cancel(self) -> None: ...
    def _release(self) -> None: ...
    def Pause(self, sec: Optional[float] = None) -> McTimer: ...
    def Continue(self) -> McTimer: ...
    def Execute(self) -> Any: ...
    def IsCanceled(self) -> bool: ...
    def IsPaused(self) -> bool: ...
