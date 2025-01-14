# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-01-09
#
# ====================================================


from typing import Callable


class TimeEaseFunc:
    linear: Callable[[float], float]
    spring: Callable[[float], float]
    in_quad: Callable[[float], float]
    out_quad: Callable[[float], float]
    in_out_quad: Callable[[float], float]
    in_cubic: Callable[[float], float]
    out_cubic: Callable[[float], float]
    in_out_cubic: Callable[[float], float]
    in_quart: Callable[[float], float]
    out_quart: Callable[[float], float]
    in_out_quart: Callable[[float], float]
    in_quint: Callable[[float], float]
    out_quint: Callable[[float], float]
    in_out_quint: Callable[[float], float]
    in_sine: Callable[[float], float]
    out_sine: Callable[[float], float]
    in_out_sine: Callable[[float], float]
    in_expo: Callable[[float], float]
    out_expo: Callable[[float], float]
    in_out_expo: Callable[[float], float]
    in_circ: Callable[[float], float]
    out_circ: Callable[[float], float]
    in_out_circ: Callable[[float], float]
    in_bounce: Callable[[float], float]
    out_bounce: Callable[[float], float]
    in_out_bounce: Callable[[float], float]
    in_back: Callable[[float], float]
    out_back: Callable[[float], float]
    in_out_back: Callable[[float], float]
    in_elastic: Callable[[float], float]
    out_elastic: Callable[[float], float]
    in_out_elastic: Callable[[float], float]


class TimeEase(object):
    start_val: float
    end_val: float
    total_tm: float
    hold_on_last_frame: bool
    fps: int
    ease_func: Callable[[float], float]
    _init_tm: float
    _frame: int
    _total_frame: int
    _stopped: bool
    def __init__(
        self,
        start_val: float,
        end_val: float,
        total_tm: float,
        fps: int = 0,
        hold_on_last_frame: bool = False,
        ease_func: Callable[[float], float] = TimeEaseFunc.linear,
    ) -> None: ...
    def __iter__(self) -> None: ...
    def __next__(self) -> None: ...
    def reset(self) -> None: ...
