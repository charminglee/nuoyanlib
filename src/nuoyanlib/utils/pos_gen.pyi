# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


from typing_extensions import Self
from abc import abstractmethod, ABCMeta
from typing import NoReturn, Iterator
from ..core._types._typing import FTuple3, ITuple3, T


class _PosGenerator(Iterator[FTuple3], metaclass=ABCMeta):
    __i: int
    len: int
    def __iter__(self: T) -> T: ...
    def next(self) -> FTuple3: ...
    def __len__(self) -> int: ...
    @abstractmethod
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
    def __init__(self: Self, pos1: FTuple3, pos2: FTuple3, count: int, only: int = -1) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_circle_pos(_PosGenerator):
    center_pos: FTuple3
    radius: float
    count: int
    __step: float
    def __init__(self: Self, center_pos: FTuple3, radius: float, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_sphere_pos(_PosGenerator):
    center_pos: FTuple3
    radius: float
    count: int
    def __init__(self: Self, center_pos: FTuple3, radius: float, count: int) -> None: ...
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
    def __init__(self: Self, pos1: FTuple3, pos2: FTuple3, count: int) -> None: ...
    def _calculate_axis_counts(self, count: int) -> ITuple3: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


class gen_spiral_pos(_PosGenerator):
    start_pos: FTuple3
    count: int
    def __init__(self: Self, start_pos: FTuple3, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...
