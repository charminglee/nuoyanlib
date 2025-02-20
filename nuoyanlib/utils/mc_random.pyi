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


from typing import Optional, Dict, Callable, Sequence, Any, Union, List
from random import Random
from .._core._typing import FTuple3


def random_pos(
    center_pos: FTuple3,
    grid: float,
    use_top_height: bool = False,
    dimension: int = 0,
) -> Optional[FTuple3]: ...
def __gen_str(choice: Callable[[Sequence], Any], s: str, l: int) -> str: ...


__random_ins: Dict[Any, Random]


def random_string(
    length: int,
    lower: bool = True,
    upper: bool =True,
    num: bool =True,
    seed: Any = None,
    generate_num: int = 1,
) -> Union[str, List[str]]: ...
def __is_pos_far_enough(
    poses: List[FTuple3],
    x: float,
    y: float,
    z: float,
    min_distance: float,
) -> bool: ...
def random_even_poses(
    center_pos: FTuple3,
    radius: float,
    pos_num: int,
    fixed_x: bool = False,
    fixed_y: bool = False,
    fixed_z: bool = False,
    min_distance: float = 1.0,
) -> List[FTuple3]: ...
