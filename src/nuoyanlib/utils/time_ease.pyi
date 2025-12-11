# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-25
|
| ====================================================
"""


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
    def __iter__(self) -> TimeEase: ...
    def _on_start(self) -> None: ...
    def _on_end(self) -> None: ...
    def next(self) -> float: ...
    def reset(self) -> None: ...
