# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-25
|
| ==============================================
"""


from typing import List
from .._core._types._typing import FTuple3


def spawn_ground_shatter_effect(
    pos: FTuple3,
    dim: int,
    r: float,
    num: int,
    block_dist: float = 1.0,
    /,
    *,
    time: float = 3.0,
    tilt_angle: float = 22.0,
    min_height: float = 0.0,
    max_height: float = 0.3,
    in_time: float = 0.2,
    out_time: float = 0.5,
    in_dist: float = 0.5,
    out_dist: float = 0.5,
) -> List[str]: ...
