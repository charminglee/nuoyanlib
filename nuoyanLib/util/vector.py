# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-14
#
# ====================================================


from math import atan as _atan, acos as _acos, pi as _pi, sin as _sin, cos as _cos
from mod.common.utils.mcmath import Vector3 as _Vector3
from .calculator import pos_distance as _pos_distance


# noinspection PyUnresolvedReferences
def vector_rot_p2p(pos1, pos2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float] | None
    """
    计算从pos1指向pos2的向量角度。
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 坐标1
    【pos2: Tuple[float, float, float]】 坐标2
    -----------------------------------------------------------
    return: Optional[Tuple[float, float]] -> 竖直角度, 水平角度
    """
    if not pos1 or not pos2:
        return
    x = pos2[0] - pos1[0]
    if x == 0:
        x = 0.000000001
    y = pos2[1] - pos1[1]
    z = pos2[2] - pos1[2]
    horiDis = _pos_distance((pos2[0], pos2[2]), (pos1[0], pos1[2]))
    if horiDis == 0:
        horiDis = 0.000000001
    horizontalRot = (_atan(z / x) / _pi) * 180
    verticalRot = (_atan(y / horiDis) / _pi) * 180 * (-1 if x < 0 else 1)
    return verticalRot, horizontalRot


# noinspection PyUnresolvedReferences
def vector_p2p(pos1, pos2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float, float] | None
    """
    计算从pos1指向pos2的单位向量。
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 坐标1
    【pos2: Tuple[float, float, float]】 坐标2
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 单位向量
    """
    if not pos1 or not pos2 or len(pos1) != len(pos2):
        return
    vector = tuple(pos2[i] - pos1[i] for i in range(len(pos1)))
    vector = _Vector3(vector)
    vector.Normalize()
    return vector.ToTuple()


# noinspection PyUnresolvedReferences
def vector_length(vector):
    # type: (tuple[float, float, float]) -> float
    """
    计算向量长度。
    -----------------------------------------------------------
    【vector: Tuple[float, float, float]】 向量
    -----------------------------------------------------------
    return: float -> 向量长度
    """
    return _Vector3(vector).Length()


# noinspection PyUnresolvedReferences
def angle_between_vectors(v1, v2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> float
    """
    计算两个向量之间的夹角。
    -----------------------------------------------------------
    【v1: Tuple[float, float, float]】 向量1
    【v2: Tuple[float, float, float]】 向量2
    -----------------------------------------------------------
    return: float -> 夹角（弧度值）
    """
    v1Len = vector_length(v1)
    v2Len = vector_length(v2)
    v1v2 = sum(i * j for i, j in zip(v1, v2))
    cos = v1v2 / (v1Len * v2Len)
    return _acos(cos)


# noinspection PyUnresolvedReferences
def rotate_vector(vector, xAngle, yAngle, zAngle):
    # type: (tuple[float, float, float], float, float, float) -> tuple[float, float, float]
    """
    计算向量旋转。
    -----------------------------------------------------------
    【vector: Tuple[float, float, float]】 向量
    【xAngle: float】 绕x轴的旋转角度
    【yAngle: float】 绕y轴的旋转角度
    【zAngle: float】 绕z轴的旋转角度
    -----------------------------------------------------------
    return: Tuple[float, float, float] -> 旋转后的向量
    """
    x1, y1, z1 = vector
    x3 = x1 * _cos(zAngle) - y1 * _sin(zAngle)
    y3 = x1 * _sin(zAngle) + y1 * _cos(zAngle)
    z3 = z1
    z4 = z3 * _cos(yAngle) - x3 * _sin(yAngle)
    x4 = z3 * _sin(yAngle) + x3 * _cos(yAngle)
    y4 = y3
    y2 = y4 * _cos(xAngle) - z4 * _sin(xAngle)
    z2 = y4 * _sin(xAngle) + z4 * _cos(xAngle)
    x2 = x4
    return x2, y2, z2


# noinspection PyUnresolvedReferences
def outgoing_vector(vector, normal):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float, float]
    """
    已知入射向量和法线求出射向量。
    -----------------------------------------------------------
    【vector: Tuple[float, float, float]】 入射向量
    【normal: Tuple[float, float, float]】 法线向量
    -----------------------------------------------------------
    return: Tuple[float, float, float] -> 出射向量
    """
    v = _Vector3(vector)
    n = _Vector3(normal)
    reflexVector = v - 2 * _Vector3.Dot(v, n) * n
    return reflexVector.ToTuple()


# noinspection PyUnresolvedReferences
def composite_vector(v1, *v2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float, float]
    """
    向量的合成。
    -----------------------------------------------------------
    【v1: Tuple[float, float, float]】 向量
    【*v2: Tuple[float, float, float]】 向量
    -----------------------------------------------------------
    return: Tuple[float, float, float] -> 合向量
    """
    resVec = _Vector3(v1)
    for v in v2:
        resVec += _Vector3(v)
    return resVec.ToTuple()






















