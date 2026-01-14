# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-13
#  ⠀
# =================================================


from typing_extensions import deprecated
from typing import List
from ..core._types._typing import FTuple3


@deprecated("由于 ModSDK 3.7 支持对客户端实体添加方块几何体，该函数即将废弃，建议使用客户端版本的同名函数。")
def spawn_ground_shatter_effect(
    pos: FTuple3,
    dim: int,
    r: float,
    num: int,
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
