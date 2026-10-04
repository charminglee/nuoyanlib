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


from nuoyanlib.common.mc_math.vector import Vector, vec_project_length
from nuoyanlib.common.mc_math import vector as _vector
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


# 投影长度：点积 / 基向量长度，与基向量模长无关（修复前错误地除以了基向量长度的平方）
assert Vector(1, 2, 3).project_length((0, 0, 2)) == 3.0
assert Vector(1, 2, 3).project_length((0, 0, 8)) == 3.0
assert Vector(2, 0, 0).project_length((0, 3, 4)) == 0.0
assert vec_project_length((2, 0), (4, 0)) == 2.0
assert vec_project_length((1, 2, 3), (0, 0, 8)) == 3.0


class _FakeRot(object):
    def __init__(self, rot):
        self._rot = rot

    def GetRot(self):
        return self._rot


class _FakeCF(object):
    def __init__(self, rot):
        self.Rot = _FakeRot(rot)


_org_get_cf = _vector.get_cf
try:
    # 水平视角（yaw=0，朝向+z，左方向为+x）
    _vector.get_cf = lambda entity_id: _FakeCF((0.0, 0.0))
    assert _vector.vec_entity_left("e") == _vector.VEC_LEFT
    assert _vector.vec_entity_right("e") == _vector.VEC_RIGHT
    assert _vector.vec_entity_up("e") == (0.0, 1.0, 0.0)

    # 俯仰角为±90°时不再抛出VectorError，退化为基于水平朝向计算
    _vector.get_cf = lambda entity_id: _FakeCF((90.0, 0.0))
    assert _vector.vec_entity_left("e") == _vector.VEC_LEFT
    assert _vector.vec_entity_right("e") == _vector.VEC_RIGHT
    u = _vector.vec_entity_up("e")
    assert u[0] == 0.0 and abs(u[1]) < 1e-15 and u[2] == 1.0

    _vector.get_cf = lambda entity_id: _FakeCF((-90.0, 0.0))
    assert _vector.vec_entity_left("e") == _vector.VEC_LEFT
    u = _vector.vec_entity_up("e")
    assert u[0] == 0.0 and abs(u[1]) < 1e-15 and u[2] == -1.0

    # 获取视角失败时返回None
    _vector.get_cf = lambda entity_id: _FakeCF(None)
    assert _vector.vec_entity_left("e") is None
    assert _vector.vec_entity_up("e") is None
finally:
    _vector.get_cf = _org_get_cf
