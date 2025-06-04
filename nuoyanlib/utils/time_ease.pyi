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


from typing import Callable


_TEType = Callable[[float], float]


class TimeEaseFunc:
    linear: _TEType
    spring: _TEType
    in_quad: _TEType
    out_quad: _TEType
    in_out_quad: _TEType
    in_cubic: _TEType
    out_cubic: _TEType
    in_out_cubic: _TEType
    in_quart: _TEType
    out_quart: _TEType
    in_out_quart: _TEType
    in_quint: _TEType
    out_quint: _TEType
    in_out_quint: _TEType
    in_sine: _TEType
    out_sine: _TEType
    in_out_sine: _TEType
    in_expo: _TEType
    out_expo: _TEType
    in_out_expo: _TEType
    in_circ: _TEType
    out_circ: _TEType
    in_out_circ: _TEType
    in_bounce: _TEType
    out_bounce: _TEType
    in_out_bounce: _TEType
    in_back: _TEType
    out_back: _TEType
    in_out_back: _TEType
    in_elastic: _TEType
    out_elastic: _TEType
    in_out_elastic: _TEType


class TimeEase(object):
    start_val: float
    end_val: float
    total_tm: float
    hold_on_last_frame: bool
    fps: int
    ease_func: _TEType
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
        ease_func: _TEType = TimeEaseFunc.linear,
    ) -> None: ...
    def __iter__(self) -> None: ...
    def next(self) -> None: ...
    def reset(self) -> None: ...
