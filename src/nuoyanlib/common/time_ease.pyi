# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


from typing import Optional, Callable, Any
from ..core._types._typing import Self, TimeEaseFuncType
from .enum import TimeEaseFunc


class TimeEase(object):
    start_val: float
    end_val: float
    total_tm: float
    hold_on_last_frame: bool
    fps: int
    ease_func: TimeEaseFuncType
    next_te: Optional[TimeEase]
    on_start: Optional[Callable[[], Any]]
    on_end: Optional[Callable[[], Any]]
    _init_tm: float
    _frame: int
    _total_frame: int
    _diff_val: float
    _val: float
    _state: int
    _is_static: bool
    def __init__(
        self: Self,
        start_val: float,
        end_val: float,
        total_tm: float,
        fps: int = 0,
        hold_on_last_frame: bool = False,
        ease_func: TimeEaseFuncType = TimeEaseFunc.LINEAR,
        next_te: Optional[TimeEase] = None,
        on_start: Optional[Callable[[], Any]] = None,
        on_end: Optional[Callable[[], Any]] = None,
    ) -> None: ...
    @staticmethod
    def static(
        val: float,
        total_tm: float,
        hold_on_last_frame: bool = False,
        next_te: Optional[TimeEase] = None,
        on_start: Optional[Callable[[], Any]] = None,
        on_end: Optional[Callable[[], Any]] = None,
    ) -> TimeEase: ...
    def __iter__(self) -> TimeEase: ...
    def _on_start(self) -> None: ...
    def _on_end(self) -> None: ...
    def __next__(self) -> float: ...
    next = __next__
    def reset(self) -> None: ...
