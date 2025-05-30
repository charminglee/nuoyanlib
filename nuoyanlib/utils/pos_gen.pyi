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
#   Last Modified : 2025-05-30
#
# ====================================================


from typing import TypeVar, NoReturn, Tuple
from .._core._types._typing import FTuple3


_T = TypeVar("_T")


class _PosGenerator(object):
    len: int
    __i: int
    def __iter__(self: _T) -> _T: ...
    def next(self) -> FTuple3: ...
    def __len__(self) -> int: ...
    def __gen_pos__(self, i: int) -> NoReturn: ...
    def __getitem__(self, i: int) -> FTuple3: ...


class gen_line_pos(_PosGenerator):
    pos1: FTuple3
    pos2: FTuple3
    count: int
    only: int
    __x_step: float
    __y_step: float
    __z_step: float
    def __init__(self, pos1: FTuple3, pos2: FTuple3, count: int, only: int = -1) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_circle_pos(_PosGenerator):
    center_pos: FTuple3
    radius: float
    count: int
    __step: float
    def __init__(self, center_pos: FTuple3, radius: float, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_sphere_pos(_PosGenerator):
    center_pos: FTuple3
    radius: float
    count: int
    def __init__(self, center_pos: FTuple3, radius: float, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_cube_pos(_PosGenerator):
    pos1: FTuple3
    pos2: FTuple3
    count: int
    __minx: float
    __miny: float
    __minz: float
    __maxx: float
    __maxy: float
    __maxz: float
    __count_x: int
    __count_y: int
    __count_z: int
    __x_step: float
    __y_step: float
    __z_step: float
    def __init__(self, pos1: FTuple3, pos2: FTuple3, count: int) -> None: ...
    def _calculate_axis_counts(self, count: int) -> Tuple[int, int, int]: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_spiral_pos(_PosGenerator):
    start_pos: FTuple3
    count: int
    def __init__(self, start_pos: FTuple3, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...
