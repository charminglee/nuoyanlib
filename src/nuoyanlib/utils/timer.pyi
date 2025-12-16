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


from typing import Callable, Any, Optional, overload, Hashable, Dict
from threading import Timer as _Timer
from mod.common.utils.timer import CallLater
from ..core._types._typing import Self, F


_c_delay_timers: Dict[Hashable, CallLater]
_s_delay_timers: Dict[Hashable, CallLater]
_c_repeat_timers: Dict[Hashable, CallLater]
_s_repeat_timers: Dict[Hashable, CallLater]


def _set_timer(t: float, func: Callable[[], Any], is_repeat: bool, key: Optional[Hashable]) -> None: ...
@overload
def delay(t: float = 0, key: Optional[Hashable] = None) -> Callable[[F], F]: ...
@overload
def delay(t: F, key: Optional[Hashable] = None) -> F: ...
@overload
def repeat(t: float = 0, key: Optional[Hashable] = None) -> Callable[[F], F]: ...
@overload
def repeat(t: F, key: Optional[Hashable] = None) -> F: ...


class Timer(object):
    type: str
    sec: float
    func: Optional[Callable]
    args: Any
    kwargs: Any
    _pause: bool
    _cancel: bool
    __timer: Optional[_Timer]
    def __init__(self: Self, ttype: str, sec: float, func: Callable, *args: Any, **kwargs: Any): ...
    def _execute(self) -> Any: ...
    def __func(self) -> None: ...
    def Start(self) -> Timer: ...
    def Cancel(self) -> None: ...
    def _release(self) -> None: ...
    def Pause(self, sec: Optional[float] = None) -> Timer: ...
    def Continue(self) -> Timer: ...
    def Execute(self) -> Any: ...
    def IsCanceled(self) -> bool: ...
    def IsPaused(self) -> bool: ...
