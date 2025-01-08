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
#   Last Modified : 2023-11-26

# ====================================================


from typing import Tuple, List


def vec_normalize(vector: Tuple[float, float, float]) -> Tuple[float, float, float]: ...
def vec_rot_p2p(
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
) -> Tuple[float, float]: ...
def vec_p2p(
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
) -> Tuple[float, float, float]: ...
def vec_length(vector: Tuple[float, float, float]) -> float: ...
def vec_angle(v1: Tuple[float, float, float], v2: Tuple[float, float, float]) -> float: ...
def _matrix_mult(matrix1: List[List[float]], matrix2: List[List[float]]) -> List[List[float]]: ...
def vec_euler_rotate(
    vector: Tuple[float, float, float],
    x_angle: float = 0.0,
    y_angle: float = 0.0,
    z_angle: float = 0.0,
    order: str = "zyx",
) -> Tuple[float, float, float]: ...
def vec_rotate_around(
    v: Tuple[float, float, float],
    u: Tuple[float, float, float],
    angle: float,
) -> Tuple[float, float, float]: ...
def outgoing_vec(
    vector: Tuple[float, float, float],
    normal: Tuple[float, float, float],
) -> Tuple[float, float, float]: ...
def vec_composite(
    vector: Tuple[float, float, float],
    *more_vec: Tuple[float, float, float],
) -> Tuple[float, float, float]: ...
