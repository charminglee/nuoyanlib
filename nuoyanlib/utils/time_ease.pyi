# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-18
|
| ==============================================
"""


from typing import Optional
from .._core._types._typing import TimeEaseFuncType


class TimeEaseFunc:
    linear: TimeEaseFuncType
    spring: TimeEaseFuncType
    in_quad: TimeEaseFuncType
    out_quad: TimeEaseFuncType
    in_out_quad: TimeEaseFuncType
    in_cubic: TimeEaseFuncType
    out_cubic: TimeEaseFuncType
    in_out_cubic: TimeEaseFuncType
    in_quart: TimeEaseFuncType
    out_quart: TimeEaseFuncType
    in_out_quart: TimeEaseFuncType
    in_quint: TimeEaseFuncType
    out_quint: TimeEaseFuncType
    in_out_quint: TimeEaseFuncType
    in_sine: TimeEaseFuncType
    out_sine: TimeEaseFuncType
    in_out_sine: TimeEaseFuncType
    in_expo: TimeEaseFuncType
    out_expo: TimeEaseFuncType
    in_out_expo: TimeEaseFuncType
    in_circ: TimeEaseFuncType
    out_circ: TimeEaseFuncType
    in_out_circ: TimeEaseFuncType
    in_bounce: TimeEaseFuncType
    out_bounce: TimeEaseFuncType
    in_out_bounce: TimeEaseFuncType
    in_back: TimeEaseFuncType
    out_back: TimeEaseFuncType
    in_out_back: TimeEaseFuncType
    in_elastic: TimeEaseFuncType
    out_elastic: TimeEaseFuncType
    in_out_elastic: TimeEaseFuncType


class TimeEase(object):
    start_val: float
    end_val: float
    total_tm: float
    hold_on_last_frame: bool
    fps: int
    ease_func: TimeEaseFuncType
    next_te: Optional[TimeEase]
    _init_tm: float
    _frame: int
    _total_frame: int
    _stopped: bool
    _diff_val: float
    def __init__(
        self,
        start_val: float,
        end_val: float,
        total_tm: float,
        fps: int = 0,
        hold_on_last_frame: bool = False,
        ease_func: TimeEaseFuncType = TimeEaseFunc.linear,
        next_te: Optional[TimeEase] = None,
    ) -> None: ...
    def __iter__(self) -> TimeEase: ...
    def _on_stop(self) -> None: ...
    def next(self) -> None: ...
    def reset(self) -> None: ...
