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
#   Last Modified : 2023-11-30
#
# ====================================================


from typing import Optional, Tuple, Dict, Callable, Sequence, Any, Union, List
from random import Random


_LEVEL_ID: str


def _is_client() -> bool: ...
def random_pos(
    center_pos: Tuple[float, float, float],
    grid: float,
    use_top_height: bool = False,
    dimension: int = 0,
) -> Optional[Tuple[float, float, float]]: ...
def _gen_str(choice: Callable[[Sequence], Any], s: str, l: int) -> str: ...


_random_ins: Dict[Any, Random]


def random_string(
    length: int,
    lower: bool = True,
    upper: bool =True,
    num: bool =True,
    seed: Any = None,
    generate_num: int = 1,
) -> Union[str, List[str]]: ...
def _is_pos_far_enough(
    poses: List[Tuple[float, float, float]],
    x: float,
    y: float,
    z: float,
    min_distance: float,
) -> bool: ...
def random_even_poses(
    center_pos: Tuple[float, float, float],
    x_range: float,
    y_range: float,
    z_range: float,
    pos_num: int,
    min_distance: float = 1.0,
) -> List[Tuple[float, float, float]]: ...