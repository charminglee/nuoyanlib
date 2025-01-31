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
#   Last Modified : 2025-01-29
#
# ====================================================


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
