# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-3-27
#  ⠀
# =================================================


from math import sin, cos, sqrt, pi
import random


__all__ = [
    "random_quat",
]


def random_quat():
    """
    生成一个随机的均匀分布的单位四元数。

    -----

    :return: 单位四元数
    :rtype: tuple[float,float,float,float]
    """
    u1 = random.random()
    u2 = random.random()
    u3 = random.random()
    sqrt_1_u1 = sqrt(1 - u1)
    sqrt_u1 = sqrt(u1)
    twopi_u2 = 2 * pi * u2
    twopi_u3 = 2 * pi * u3
    return (
        sqrt_1_u1 * cos(twopi_u2),
        sqrt_u1 * sin(twopi_u3),
        sqrt_u1 * cos(twopi_u3),
        sqrt_1_u1 * sin(twopi_u2),
    )






















