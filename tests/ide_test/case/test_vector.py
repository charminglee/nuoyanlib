# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from nuoyanlib.common.mc_math.vector import Vector
from nuoyanlib.core._utils import assert_error
from nuoyanlib.core.error import VectorError


v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)


assert Vector(1, 2, 3) == Vector((1, 2, 3))
assert v1.normalize(False).length == 1
assert v1[0] == 1
assert tuple(v1) == (1, 2, 3)


assert_error(v1.dot, ((1, 2),), exc=VectorError)
assert v1.dot(v2) == v1.dot((4, 5, 6)) == 32
assert v1.cross(v2, False) == v1.cross((4, 5, 6), False) == (-3, 6, -3)


assert -v1 == (-1, -2, -3)
v1.neg() # Vector(-1, -2, -3)
assert v1 == (-1, -2, -3)


assert v1 + v2 == v1 + (4, 5, 6) == (3, 3, 3)
assert v1 + 1 == (0, -1, -2)
assert 1 + v1 == (0, -1, -2)
v1 += 1 # Vector(0, -1, -2)
assert v1 == (0, -1, -2)
v1 += (1, 1, 1) # Vector(1, 0, -1)
assert v1 == (1, 0, -1)


assert v1 - v2 == v1 - (4, 5, 6) == (-3, -5, -7)
assert v1 - 1 == (0, -1, -2)
assert 1 - v1 == (0, 1, 2)
v1 -= 1 # Vector(0, -1, -2)
assert v1 == (0, -1, -2)
v1 -= (1, 1, 1) # Vector(-1, -2, -3)
assert v1 == (-1, -2, -3)


assert v1 * 2 == (-2, -4, -6)
assert 2 * v1 == (-2, -4, -6)
v1 *= 2 # Vector(-2, -4, -6)
assert v1 == (-2, -4, -6)


assert v1 / 2.0 == (-1, -2, -3)
v1 /= 2.0 # Vector(-1, -2, -3)
assert v1 == (-1, -2, -3)


assert v1 // 1.5 == (-1, -2, -2)
v1 //= 1.5 # Vector(-1, -2, -2)
assert v1 == (-1, -2, -2)


v1[0] = 7
v1[1] = 8
v1[2] = 9
assert v1 == (7, 8, 9)
