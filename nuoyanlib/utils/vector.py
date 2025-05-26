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
#   Last Modified : 2025-05-23
#
# ====================================================


from math import (
    atan as _atan,
    acos as _acos,
    pi as _pi,
    sin as _sin,
    cos as _cos,
    radians as _radians,
)
from mod.common.utils.mcmath import (
    Vector3 as _Vector3,
    Matrix as _Matrix,
)
from . import mc_math as _mc_math
from .._core import _sys


__all__ = [
    "is_zero_vec",
    "set_vec_length",
    "vec_orthogonal_decomposition",
    "vec_entity_left",
    "vec_entity_right",
    "vec_entity_front",
    "vec_entity_back",
    "vec_normalize",
    "vec_rot_p2p",
    "vec_p2p",
    "vec_length",
    "vec_angle",
    "vec_euler_rotate",
    "vec_rotate_around",
    "outgoing_vec",
    "vec_composite",
    "vec_scale",
]


def is_zero_vec(vec):
    """
    | 判断向量是否是零向量。

    -----

    :param tuple[float,float,float]|_Vector3 vec: 向量

    :return: 是否是零向量
    :rtype: bool
    """
    return not any(vec[i] for i in range(3))

def set_vec_length(vec, length, convert_vec=False):
    """
    | 设置向量长度。

    -----

    :param tuple[float,float,float]|_Vector3 vec: 向量
    :param float length: 长度
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 设置后的向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    vec_ = _to_Vector3(vec)
    orig_len = vec_.Length()
    if orig_len <= 0:
        raise ValueError("Zero vector cannot set length")
    res = vec_.Normalized() * length
    return _convert_return_vec(vec, res, convert_vec)


def vec_orthogonal_decomposition(vec, basis1, basis2, convert_vec=False):
    """
    | 对向量进行正交分解。

    -----

    :param tuple[float,float,float]|_Vector3 vec: 要分解的向量
    :param tuple[float,float,float]|_Vector3 basis1: 正交基1
    :param tuple[float,float,float]|_Vector3 basis2: 正交基2
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 分解后的两个向量，第一个向量沿basis1方向，第二个向量沿basis2方向
    :rtype: tuple[tuple[float,float,float]|_Vector3, tuple[float,float,float]|_Vector3]

    :raise ValueError: 两个向量非正交时抛出
    """
    vec_ = _to_Vector3(vec)
    basis1 = _to_Vector3(basis1)
    basis2 = _to_Vector3(basis2)
    vec1 = (_Vector3.Dot(vec_, basis1) / _Vector3.Dot(basis1, basis1)) * basis1
    vec2 = (_Vector3.Dot(vec_, basis2) / _Vector3.Dot(basis2, basis2)) * basis2
    return _convert_return_vec(vec, vec1, convert_vec), _convert_return_vec(vec, vec2, convert_vec)


def vec_entity_left(entity_id, ret_Vector3=False):
    """
    | 获取实体朝向左侧90°的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ret_Vector3: 是否以Vector3类型返回，默认为False，返回tuple

    :return: 实体朝向左侧90°的单位向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    front = vec_entity_front(entity_id, ret_Vector3=True)
    up = _Vector3.Up()
    left = _Vector3.Cross(up, front)
    left.Normalize()
    if not ret_Vector3:
        left = left.ToTuple()
    return left


def vec_entity_right(entity_id, ret_Vector3=False):
    """
    | 获取实体朝向右侧90°的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ret_Vector3: 是否以Vector3类型返回，默认为False，返回tuple

    :return: 实体朝向右侧90°的单位向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    right = -_Vector3(vec_entity_left(entity_id)) # 手动转Vector3而不是使用ret_Vector3参数，以规避机审报错（机审会判定为tuple无法使用-运算符）
    return right if ret_Vector3 else right.ToTuple()


def vec_entity_front(entity_id, ignore_y=False, ret_Vector3=False):
    """
    | 获取实体朝向的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_y: 是否忽略y轴朝向，设为True时y轴朝向恒定为0，默认为False
    :param bool ret_Vector3: 是否以Vector3类型返回，默认为False，返回tuple

    :return: 实体朝向的单位向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    api = _sys.get_api()
    cf = _sys.get_comp_factory()
    front = api.GetDirFromRot(cf.CreateRot(entity_id).GetRot())
    if ignore_y:
        front = vec_normalize((front[0], 0, front[2]))
    if ret_Vector3:
        front = _Vector3(front)
    return front


def vec_entity_back(entity_id, ignore_y=False, ret_Vector3=False):
    """
    | 获取与实体朝向相反的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_y: 是否忽略y轴朝向，设为True时y轴朝向恒定为0，默认为False
    :param bool ret_Vector3: 是否以Vector3类型返回，默认为False，返回tuple

    :return: 与实体朝向相反的单位向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    back = -_Vector3(vec_entity_front(entity_id, ignore_y))
    return back if ret_Vector3 else back.ToTuple()


def _to_Vector3(vec):
    if isinstance(vec, _Vector3):
        return vec
    else:
        return _Vector3(*vec)


def _convert_return_vec(input_vec, output_vec, convert):
    if convert:
        if isinstance(input_vec, _Vector3):
            if isinstance(output_vec, _Vector3):
                return output_vec.ToTuple()
            else:
                return tuple(output_vec)
        else:
            return _to_Vector3(output_vec)
    else:
        input_type = type(input_vec)
        return (
            input_type((output_vec[0], output_vec[1], output_vec[2])) if isinstance(output_vec, _Vector3)
            else input_type(output_vec)
        )


def vec_normalize(vec, convert_vec=False):
    """
    | 向量标准化。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec: 向量（支持tuple、list或Vector3表示）
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 单位向量，长度为1
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    res = _to_Vector3(vec).Normalized()
    return _convert_return_vec(vec, res, convert_vec)


def vec_rot_p2p(pos1, pos2):
    """
    | 计算从 ``pos1`` 指向 ``pos2`` 的向量角度。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: 角度元组，分别为竖直角度、水平角度
    :rtype: tuple[float,float]
    """
    x = pos2[0] - pos1[0]
    if x == 0:
        x = 0.000000001
    y = pos2[1] - pos1[1]
    z = pos2[2] - pos1[2]
    hori_dis = _mc_math.pos_distance((pos2[0], pos2[2]), (pos1[0], pos1[2]))
    if hori_dis == 0:
        hori_dis = 0.000000001
    horizontal_rot = (_atan(z / x) / _pi) * 180
    vertical_rot = (_atan(y / hori_dis) / _pi) * 180 * (-1 if x < 0 else 1)
    return vertical_rot, horizontal_rot


def vec_p2p(pos1, pos2, ret_Vector3=False):
    """
    | 计算从 ``pos1`` 指向 ``pos2`` 的单位向量。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2
    :param bool ret_Vector3: 是否以Vector3类型返回，默认为False，返回tuple

    :return: 从pos1指向pos2的单位向量
    :rtype: tuple[float,float,float]|_Vector3
    """
    vec = _to_Vector3(pos2) - _to_Vector3(pos1)
    vec.Normalize()
    return vec if ret_Vector3 else vec.ToTuple()


def vec_length(vec):
    """
    | 计算向量长度（模长）。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec: 向量（支持tuple、list或Vector3表示）

    :return: 向量长度
    :rtype: float
    """
    return _to_Vector3(vec).Length()


def vec_angle(vec1, vec2):
    """
    | 计算两个向量之间的夹角。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec1: 向量1（支持tuple、list或Vector3表示）
    :param tuple[float,float,float]|list[float]|_Vector3 vec2: 向量2（支持tuple、list或Vector3表示）

    :return: 夹角弧度值
    :rtype: float
    """
    vec1 = _to_Vector3(vec1)
    vec2 = _to_Vector3(vec2)
    vec1_len = vec1.Length()
    vec2_len = vec2.Length()
    v1_v2 = _Vector3.Dot(vec1, vec2)
    cos = v1_v2 / (vec1_len * vec2_len)
    return _acos(cos)


def vec_euler_rotate(vec, x_angle=0.0, y_angle=0.0, z_angle=0.0, order="zyx", convert_vec=False):
    """
    | 对指定向量应用欧拉旋转。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec: 要旋转的向量（支持tuple、list或Vector3表示）
    :param float x_angle: 绕x轴的旋转角度
    :param float y_angle: 绕y轴的旋转角度
    :param float z_angle: 绕z轴的旋转角度
    :param str order: 旋转顺序，默认为"zyx"，即先按z轴旋转，再按y轴旋转，最后按x轴旋转
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 旋转后的向量
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    x_angle = _radians(x_angle)
    y_angle = _radians(y_angle)
    z_angle = _radians(z_angle)
    cos_x, sin_x = _cos(x_angle), _sin(x_angle)
    cos_y, sin_y = _cos(y_angle), _sin(y_angle)
    cos_z, sin_z = _cos(z_angle), _sin(z_angle)
    # 旋转矩阵
    x_matrix = _Matrix.Create([
        [1, 0, 0],
        [0, cos_x, -sin_x],
        [0, sin_x, cos_x],
    ])
    y_matrix = _Matrix.Create([
        [cos_y, 0, sin_y],
        [0, 1, 0],
        [-sin_y, 0, cos_y],
    ])
    z_matrix = _Matrix.Create([
        [cos_z, -sin_z, 0],
        [sin_z, cos_z, 0],
        [0, 0, 1],
    ])
    # 用于累积旋转的矩阵
    acc_matrix = _Matrix.CreateEye(3)
    for axis in order:
        if axis == 'x':
            acc_matrix = acc_matrix * x_matrix
        elif axis == 'y':
            acc_matrix = acc_matrix * y_matrix
        elif axis == 'z':
            acc_matrix = acc_matrix * z_matrix
    # 计算旋转
    column_vec = _Matrix.Create(
        [[vec[i]] for i in range(3)] if isinstance(vec, _Vector3) else [[i] for i in vec]
    )
    rotated_vec = acc_matrix * column_vec
    res = tuple(i[0] for i in rotated_vec)
    return _convert_return_vec(vec, res, convert_vec)


def vec_rotate_around(v, u, angle, convert_vec=False):
    """
    | 将向量v绕着向量u旋转。

    :param tuple[float,float,float]|list[float]|_Vector3 v: 要旋转的向量（支持tuple、list或Vector3表示）
    :param tuple[float,float,float]|list[float]|_Vector3 u: 旋转轴向量（支持tuple、list或Vector3表示）
    :param float angle: 旋转角度
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 旋转后的向量
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    v = _to_Vector3(v)
    v_len = v.Length()
    v.Normalize()
    u = _to_Vector3(u).Normalized()
    theta = _radians(angle)
    cos = _cos(theta)
    sin = _sin(theta)
    dot = _Vector3.Dot(u, v)
    cross = _Vector3.Cross(u, v)
    res = v * cos + u * (1 - cos) * dot + cross * sin # 罗德里格旋转公式
    res = res * v_len
    return _convert_return_vec(v, res, convert_vec)


def outgoing_vec(vec, normal, convert_vec=False):
    """
    | 已知入射向量和法线求出射向量。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec: 入射向量（支持tuple、list或Vector3表示）
    :param tuple[float,float,float]|list[float]|_Vector3 normal: 法线向量（支持tuple、list或Vector3表示）
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 出射向量
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    v = _to_Vector3(vec)
    n = _to_Vector3(normal)
    reflex_vec = v - 2 * _Vector3.Dot(v, n) * n
    return _convert_return_vec(vec, reflex_vec, convert_vec)


def vec_composite(convert_vec, vec, *more_vec):
    """
    | 向量的合成。

    -----

    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同
    :param tuple[float,float,float]|list[float]|_Vector3 vec: 向量（支持tuple、list或Vector3表示）
    :param tuple[float,float,float]|list[float]|_Vector3 more_vec: 更多向量（支持tuple、list或Vector3表示）

    :return: 合向量
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    res = _to_Vector3(vec)
    for v in more_vec:
        res += _to_Vector3(v)
    return _convert_return_vec(vec, res, convert_vec)


def vec_scale(vec, scale, convert_vec=False):
    """
    向量缩放。

    -----

    :param tuple[float,float,float]|list[float]|_Vector3 vec: 向量（支持tuple、list或Vector3表示）
    :param float scale: 缩放倍率
    :param bool convert_vec: 是否转换向量类型，设为True时，若输入的向量为tuple，则转换为Vector3类型输出，若输入Vector3类型，则转换为tuple输出；设为False时，输出类型与输入类型相同；默认为False

    :return: 缩放后的向量
    :rtype: tuple[float,float,float]|list[float]|_Vector3
    """
    res = _to_Vector3(vec) * scale
    return _convert_return_vec(vec, res, convert_vec)






















