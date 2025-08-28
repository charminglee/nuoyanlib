# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-19
|
| ==============================================
"""


from typing import Optional, Any, Union, List
from .._core._types._typing import FTuple3


def random_pos(center_pos: FTuple3, r: float, dim: int = 0, use_top_height: bool = False) -> Optional[FTuple3]: ...
def random_string(
    length: int,
    lower: bool = True,
    upper: bool =True,
    num: bool =True,
    seed: Any = None,
    generate_num: int = 1,
) -> Union[str, List[str]]: ...
def random_even_poses(
    center_pos: FTuple3,
    radius: float,
    pos_num: int,
    fixed_x: bool = False,
    fixed_y: bool = False,
    fixed_z: bool = False,
    min_distance: float = 1.0,
) -> List[FTuple3]: ...
