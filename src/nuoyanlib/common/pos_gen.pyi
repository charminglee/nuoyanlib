# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-10
#  ⠀
# =================================================


from typing import Tuple, Any, Dict, Generic, Iterator, Generator, List, Literal, Optional, overload
from random import Random
from ..core._types._typing import Self, FTuple3, ITuple3, SlotsType, PosT, ITuple2, FTuple2


class _PosGenerator(Generic[PosT]):
    count: int
    def __init__(self: Self) -> None: ...
    def __iter__(self) -> Iterator[PosT]: ...
    def __len__(self) -> int: ...
    def __gen_pos__(self, i: int) -> PosT: ...
    @overload
    def __getitem__(self, item: slice) -> Generator[PosT]: ...
    @overload
    def __getitem__(self, item: int) -> PosT: ...


class gen_random_even_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    _spawned: Dict[int, PosT]
    _uniform = Random.uniform
    _random = Random.random
    center: PosT
    radius: float
    count: int
    fixed_x: bool
    fixed_y: bool
    fixed_z: bool
    def __init__(
        self: Self,
        center: PosT,
        radius: float,
        count: int,
        fixed_x: bool = False,
        fixed_y: bool = False,
        fixed_z: bool = False,
        seed: Optional[Any] = None,
    ) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...


def _gen_line_pos(start: PosT, i: int, x_step: float = 0, y_step: float = 0, z_step: float = 0) -> PosT: ...


class gen_line_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    _x_step: float
    _y_step: float
    _z_step: float
    start: PosT
    end: PosT
    count: int
    def __init__(self: Self, start: PosT, end: PosT, count: int) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...


class gen_ring_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    _step: float
    center: PosT
    radius: float
    count: int
    axis_dir: Literal["x", "y", "z"]
    def __init__(self: Self, center: PosT, radius: float, count: int, axis_dir: Literal["x", "y", "z"]) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...


_GOLDEN_RATIO: float


class gen_sphere_pos(_PosGenerator[FTuple3]):
    __slots__: SlotsType
    _fixed_count: int
    center: FTuple3
    radius: float
    count: int
    fixed_x: bool
    fixed_y: bool
    fixed_z: bool
    def __init__(
        self: Self,
        center: FTuple3,
        radius: float,
        count: int,
        fixed_x: bool = False,
        fixed_y: bool = False,
        fixed_z: bool = False,
    ) -> None: ...
    def __gen_pos__(self, i: int) -> FTuple3: ...


@overload
def _calc_axis_counts(min_pos: FTuple3, max_pos: FTuple3, count: int) -> ITuple3: ...
@overload
def _calc_axis_counts(min_pos: FTuple2, max_pos: FTuple2, count: int) -> ITuple2: ...


class gen_box_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    _min_pos: PosT
    _count_x: int
    _count_y: int
    _x_step: float
    _y_step: float
    _z_step: float
    pos1: PosT
    pos2: PosT
    interval: float
    count: int
    def __init__(self: Self, pos1: PosT, pos2: PosT, interval: float) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...


class gen_box_surface_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    _min_pos: PosT
    _step_x: float
    _step_y: float
    _step_z: float
    pos1: PosT
    pos2: PosT
    count_x: int
    count_y: int
    count_z: int
    count: int
    def __init__(self: Self, pos1: PosT, pos2: PosT, count_x: int, count_y: int, count_z: int) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...


class gen_box_frame_pos(_PosGenerator[PosT]):
    __slots__: SlotsType
    pos1: PosT
    pos2: PosT
    count_x: int
    count_y: int
    count_z: int
    count: int
    _vertices: List[PosT]
    _segments: List[Tuple[int, PosT, PosT]]
    _dim: int
    def __init__(self: Self, pos1: PosT, pos2: PosT, count_x: int = 1, count_y: int = 1, count_z: int = 1) -> None: ...
    def __gen_pos__(self, i: int) -> PosT: ...
