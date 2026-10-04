# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-10-4
#  ⠀
#  ================================================


from math import degrees, atan2, radians, sin, cos, sqrt
from nuoyanlib.common.mc_math.mc_math import polar_coord, cartesian_coord


# 传入 None 时返回 None
assert polar_coord(None) is None
assert cartesian_coord(None) is None


# 默认原点：2D
assert polar_coord((3, 4)) == (5.0, degrees(atan2(4, 3)))
assert polar_coord((3, 4), True) == (5.0, atan2(4, 3))
# 默认原点：3D（修复前默认 origin=(0, 0)，3D 坐标会抛出 IndexError）
assert polar_coord((0, 3, 4)) == (5.0, degrees(atan2(3, 4)), degrees(atan2(3, 0)))
assert polar_coord((0, 3, 4), True) == (5.0, atan2(3, 4), atan2(3, 0))


# 自定义原点：2D
assert polar_coord((3, 4), origin=(1, 1)) == (sqrt(2**2 + 3**2), degrees(atan2(3, 2)))
# 自定义原点：3D
assert polar_coord((0, 3, 4), origin=(0, 1, 2)) == (sqrt(2**2 + 2**2), degrees(atan2(2, 2)), degrees(atan2(2, 0)))


# 默认原点：2D（修复前 origin 默认为 None，会抛出 TypeError）
assert cartesian_coord((5, 90)) == (5 * cos(radians(90)), 5 * sin(radians(90)))
assert cartesian_coord((5, radians(90)), True) == (5 * cos(radians(90)), 5 * sin(radians(90)))
# 默认原点：3D
assert cartesian_coord((5, 30, 60)) == (
    5 * sin(radians(30)) * cos(radians(60)),
    5 * sin(radians(30)) * sin(radians(60)),
    5 * cos(radians(30)),
)


# 自定义原点：2D
assert cartesian_coord((2, 0), origin=(10, 20)) == (12.0, 20.0)
# 自定义原点：3D
assert cartesian_coord((2, 0, 0), origin=(10, 20, 30)) == (10.0, 20.0, 32.0)
