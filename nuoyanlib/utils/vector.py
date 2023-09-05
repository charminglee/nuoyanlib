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
#   Last Modified : 2023-09-06

# ====================================================


from math import (
    atan as _atan,
    acos as _acos,
    pi as _pi,
    sin as _sin,
    cos as _cos,
    radians as _radians,
)
from mod.common.utils.mcmath import Vector3 as _Vector3
from calculator import pos_distance as _pos_distance


__all__ = [
    "normalize_vector",
    "vector_rot_p2p",
    "vector_p2p",
    "vector_length",
    "vector_angle",
    "rotate_vector",
    "outgoing_vector",
    "composite_vector",
]


def normalize_vector(vector):
    """
    向量标准化。支持二维向量和三维向量。

    -----

    :param tuple[float,float]|tuple[float,float,float] vector: 向量

    :return: 标准化的向量，长度为1
    :rtype: tuple[float,float]|tuple[float,float,float]
    """
    length = vector_length(vector)
    return tuple(x / length for x in vector)


def vector_rot_p2p(pos1, pos2):
    """
    计算从pos1指向pos2的向量角度。

    -----

    :param tuple[float,float,float] pos1: 三维坐标1
    :param tuple[float,float,float] pos2: 三维坐标2

    :return: 角度元组，分别为竖直角度、水平角度
    :rtype: tuple[float,float]
    """
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


def vector_p2p(pos1, pos2):
    """
    计算从pos1指向pos2的单位向量。支持二维坐标和三维坐标。

    -----

    :param tuple[float,float]|tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float]|tuple[float,float,float] pos2: 坐标2

    :return: 从pos1指向pos2的单位向量
    :rtype: tuple[float,float]|tuple[float,float,float]
    """
    vector = tuple(b - a for a, b in zip(pos1, pos2))
    return normalize_vector(vector)


def vector_length(vector):
    """
    计算向量长度。支持二维向量和三维向量。

    -----

    :param vector: tuple[float,float]|tuple[float,float,float] 向量

    :return: 向量长度
    :rtype: float
    """
    if len(vector) == 2:
        vector += (0.0,)
    return _Vector3(vector).Length()


def vector_angle(v1, v2):
    """
    计算两个向量之间的夹角。支持二维向量和三维向量。

    -----

    :param tuple[float,float]|tuple[float,float,float] v1: 向量1
    :param tuple[float,float]|tuple[float,float,float] v2: 向量2

    :return: 夹角弧度值
    :rtype: float
    """
    if len(v1) == 2:
        v1 += (0.0,)
    if len(v2) == 2:
        v2 += (0.0,)
    v1 = _Vector3(v1)
    v2 = _Vector3(v2)
    v1Len = v1.Length()
    v2Len = v2.Length()
    v1v2 = _Vector3.Dot(v1, v2)
    cos = v1v2 / (v1Len * v2Len)
    return _acos(cos)


def _matrix_mult(matrix1, matrix2):
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])
    matrix3 = [[0] * cols2 for _ in range(rows1)]
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                matrix3[i][j] += matrix1[i][k] * matrix2[k][j]
    return matrix3


def rotate_vector(vector, xAngle=0.0, yAngle=0.0, zAngle=0.0, order="xyz"):
    """
    计算向量旋转。

    -----

    :param tuple[float,float,float] vector: 三维向量
    :param float xAngle: 绕x轴的旋转角度
    :param float yAngle: 绕y轴的旋转角度
    :param float zAngle: 绕z轴的旋转角度
    :param str order: 旋转顺序，默认为"xyz"，即先选转x轴，再旋转y轴，最后旋转z轴

    :return: 旋转后的向量
    :rtype: tuple[float,float,float]
    """
    xAngle = _radians(xAngle)
    yAngle = _radians(yAngle)
    zAngle = _radians(zAngle)
    cosX, sinX = _cos(xAngle), _sin(xAngle)
    cosY, sinY = _cos(yAngle), _sin(yAngle)
    cosZ, sinZ = _cos(zAngle), _sin(zAngle)
    # 旋转矩阵
    xMatrix = [
        [1, 0, 0],
        [0, cosX, -sinX],
        [0, sinX, cosX],
    ]
    yMatrix = [
        [cosY, 0, sinY],
        [0, 1, 0],
        [-sinY, 0, cosY],
    ]
    zMatrix = [
        [cosZ, -sinZ, 0],
        [sinZ, cosZ, 0],
        [0, 0, 1],
    ]
    # 单位矩阵，用于累积旋转
    accMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for axis in order:
        if axis == 'x':
            accMatrix = _matrix_mult(accMatrix, xMatrix)
        elif axis == 'y':
            accMatrix = _matrix_mult(accMatrix, yMatrix)
        elif axis == 'z':
            accMatrix = _matrix_mult(accMatrix, zMatrix)
    # 计算旋转
    columnVector = [[i] for i in vector]
    rotatedVector = _matrix_mult(accMatrix, columnVector)
    return tuple(i[0] for i in rotatedVector)


def outgoing_vector(vector, normal):
    """
    已知入射向量和法线求出射向量。只支持三维向量。

    -----

    :param tuple[float,float,float] vector: 入射向量
    :param tuple[float,float,float] normal: 法线向量

    :return: 出射向量
    :rtype: tuple[float,float,float]
    """
    v = _Vector3(vector)
    n = _Vector3(normal)
    reflexVector = v - 2 * _Vector3.Dot(v, n) * n
    return reflexVector.ToTuple()


def composite_vector(vector, *moreVec):
    """
    向量的合成。支持二维向量和三维向量。

    -----

    :param tuple[float,float]|tuple[float,float,float] vector: 向量
    :param tuple[float,float]|tuple[float,float,float] moreVec: 更多向量

    :return: 合向量
    :rtype: tuple[float,float]|tuple[float,float,float]
    """
    if len(vector) == 2:
        vector += (0.0,)
    resVec = _Vector3(vector)
    for v in moreVec:
        if len(v) == 2:
            v += (0.0,)
        resVec += _Vector3(v)
    return resVec.ToTuple()






















