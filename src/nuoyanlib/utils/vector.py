# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


from __future__ import division
import operator
from math import degrees, sin, cos, acos, sqrt, radians, atan2
from mod.common.utils.mcmath import Matrix
from ..core._sys import get_cf
from ..core.error import VectorError


__all__ = [
    "VEC_ZERO",
    "VEC_ONE",
    "VEC_UP",
    "VEC_DOWN",
    "VEC_LEFT",
    "VEC_RIGHT",
    "VEC_FORWARD",
    "VEC_BACKWARD",
    "Vector",
    "dir2rot",
    "rot2dir",
    "dir_from_to",
    "vec_length2",
    "vec_length",
    "set_vec_length",
    "vec_normalize",
    "is_zero_vec",
    "vec_neg",
    "vec_add",
    "vec_sub",
    "vec_mul",
    "vec_div",
    "vec_dot",
    "vec_cross",
    "vec_project",
    "vec_project_length",
    "vec_angle_between",
    "vec_euler_rotate",
    "vec_rotate_around",
    "vec_entity_up",
    "vec_entity_down",
    "vec_entity_left",
    "vec_entity_right",
    "vec_entity_forward",
    "vec_entity_backward",
    "outgoing_vec",
]


_ZERO_EPS = 1e-8


VEC_ZERO     = (0.0, 0.0, 0.0)
VEC_ONE      = (1.0, 1.0, 1.0)
VEC_UP       = (0.0, 1.0, 0.0)
VEC_DOWN     = (0.0, -1.0, 0.0)
VEC_LEFT     = (1.0, 0.0, 0.0)
VEC_RIGHT    = (-1.0, 0.0, 0.0)
VEC_FORWARD  = (0.0, 0.0, 1.0)
VEC_BACKWARD = (0.0, 0.0, -1.0)


# region Vector Class ==================================================================================================


_OP_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
}


class Vector(object):
    """
    向量类，支持三维向量与二维向量。

    示例
    ----

    构造向量：

    >>> Vector(1, 2, 3) # 三维向量
    Vector(1.0, 2.0, 3.0)

    >>> Vector(1, 2) # 二维向量
    Vector(1.0, 2.0)

    >>> Vector() # 三维零向量
    Vector(0.0, 0.0, 0.0)

    从可迭代对象构造（如列表、元组、生成器等）：

    >>> vec = [1, 2, 3]
    >>> Vector(vec)
    Vector(1.0, 2.0, 3.0)
    >>> Vector(v * 2 for v in vec)
    Vector(2.0, 4.0, 6.0)

    -----

    :raise VectorError: 传入的参数不合法
    """

    __slots__ = ('_x', '_y', '_z', '_dim')

    def __init__(self, *args):
        l = len(args)
        if l == 0:
            self._x = self._y = self._z = 0.0
            self._dim = 3
            return
        if l == 1:
            vec = args[0]
            if len(vec) == 2: # noqa
                self._x, self._y = vec
                self._z = 0.0
                self._dim = 2
            else:
                self._x, self._y, self._z = vec
                self._dim = 3
            return
        if l == 2:
            self._x, self._y = args
            self._z = 0.0
            self._dim = 2
            return
        if l == 3:
            self._x, self._y, self._z = args
            self._dim = 3
            return
        raise VectorError("invalid Vector construction arguments: {}".format(args))

    @staticmethod
    def zero(is_3d=True):
        """
        [静态方法]

        创建一个零向量。

        -----

        :param bool is_3d: 是否创建三维向量；默认为 True

        :return: 零向量
        :rtype: Vector
        """
        return Vector(VEC_ZERO) if is_3d else Vector(VEC_ZERO[:2])

    @staticmethod
    def one(is_3d=True):
        """
        [静态方法]

        创建一个所有分量均为 ``1.0`` 的向量。

        -----

        :param bool is_3d: 是否创建三维向量；默认为 True

        :return: 所有分量均为 1.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_ONE) if is_3d else Vector(VEC_ONE[:2])

    @staticmethod
    def left(is_3d=True):
        """
        [静态方法]

        创建一个x分量为 ``1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否创建三维向量

        :return: x分量为 1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_LEFT) if is_3d else Vector(VEC_LEFT[:2])

    @staticmethod
    def right(is_3d=True):
        """
        [静态方法]

        创建一个x分量为 ``-1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否创建三维向量；默认为 True

        :return: x分量为 -1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_RIGHT) if is_3d else Vector(VEC_RIGHT[:2])

    @staticmethod
    def up(is_3d=True):
        """
        [静态方法]

        创建一个y分量为 ``1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否创建三维向量；默认为 True

        :return: y分量为 1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_UP) if is_3d else Vector(VEC_UP[:2])

    @staticmethod
    def down(is_3d=True):
        """
        [静态方法]

        创建一个y分量为 ``-1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否创建三维向量；默认为 True

        :return: y分量为 1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_DOWN) if is_3d else Vector(VEC_DOWN[:2])

    @staticmethod
    def forward():
        """
        [静态方法]

        创建一个z分量为 ``1.0`` ，其余分量为 ``0.0`` 的三维向量。

        -----

        :return: z分量为 1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_FORWARD)

    @staticmethod
    def backward():
        """
        [静态方法]

        创建一个z分量为 ``-1.0`` ，其余分量为 ``0.0`` 的三维向量。

        -----

        :return: z分量为 -1.0，其余分量为 0.0 的向量
        :rtype: Vector
        """
        return Vector(VEC_BACKWARD)

    @property
    def dim(self):
        """
        [只读属性]

        向量维度。

        :rtype: int
        """
        return self._dim

    @property
    def x(self):
        """
        [可读写属性]

        向量的x分量。

        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, val):
        """
        [可读写属性]

        设置向量的x分量。

        :type val: float
        """
        self._x = val

    @property
    def y(self):
        """
        [可读写属性]

        向量的y分量。

        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, val):
        """
        [可读写属性]

        设置向量的y分量。

        :type val: float
        """
        self._y = val

    @property
    def z(self):
        """
        [可读写属性]

        向量的z分量。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: float
        """
        return self._z

    @z.setter
    def z(self, val):
        """
        [可读写属性]

        设置向量的z分量。

        :type val: float
        :raise VectorError: 若向量为二维向量则抛出
        """
        if self._dim == 2:
            raise VectorError("2D vector has no z-component")
        self._z = val

    @property
    def xy(self):
        """
        [只读属性]

        返回由向量xy分量组成的元组 ``(vec.x,⠀vec.y)`` 。

        :rtype: tuple[float,float]
        """
        return self._x, self._y

    @property
    def xz(self):
        """
        [只读属性]

        返回由向量xz分量组成的元组 ``(vec.x,⠀vec.z)`` 。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float]
        """
        return self._x, self._z

    @property
    def yz(self):
        """
        [只读属性]

        返回由向量yz分量组成的元组 ``(vec.y,⠀vec.z)`` 。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float]
        """
        return self._y, self._z

    @property
    def xyz(self):
        """
        [只读属性]

        返回由向量xyz分量组成的元组 ``(vec.x,⠀vec.y,⠀vec.z)`` 。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float,float]
        """
        return self._x, self._y, self._z

    @property
    def T(self):
        """
        [只读属性]

        向量转置。

        说明
        ----

        以列表返回当前向量的列向量形式，例如：

        >>> vec = Vector(1, 2, 3)
        >>> vec.T
        [[1.0], [2.0], [3.0]]

        :rtype: list[list[float]]
        """
        return [[self._x], [self._y]] if self._dim == 2 else [[self._x], [self._y], [self._z]]

    @property
    def length2(self):
        """
        [只读属性]

        向量长度的平方。

        相比于直接计算长度，速度更快。

        :rtype: float
        """
        l = self._x**2 + self._y**2 + self._z**2
        return 0.0 if abs(l) < _ZERO_EPS else l

    @property
    def length(self):
        """
        [可读写属性]

        向量长度。

        :rtype: float
        """
        return sqrt(self.length2)

    @length.setter
    def length(self, val):
        """
        [可读写属性]

        设置向量长度。

        :type val: float
        :raise VectorError: 对零向量调用时抛出
        """
        l = self.length
        if l == 0:
            raise VectorError("can't set the length of zero vector")
        mul = val / l
        self._x *= mul
        self._y *= mul
        self._z *= mul

    def is_zero(self):
        """
        判断向量是否是零向量。

        -----

        :return: 是否是零向量
        :rtype: bool
        """
        return abs(self._x) < _ZERO_EPS and abs(self._y) < _ZERO_EPS and abs(self._z) < _ZERO_EPS

    def normalize(self, inplace=True):
        """
        向量标准化。

        -----

        :param bool inplace: 是否就地修改；默认为 True

        :return: 标准化向量，长度为 1；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 对零向量调用时抛出
        """
        l = self.length
        if l == 0:
            raise VectorError("can't normalize zero vector")
        x = self._x / l
        y = self._y / l
        z = self._z / l
        if inplace:
            self._x, self._y, self._z = x, y, z
            return self
        else:
            return Vector(x, y) if self._dim == 2 else Vector(x, y, z)

    def __neg__(self):
        """
        向量取反（返回新向量）。

        -----

        :return: 相反向量
        :rtype: Vector
        """
        return Vector(-self._x, -self._y) if self._dim == 2 else Vector(-self._x, -self._y, -self._z)

    def neg(self, inplace=True):
        """
        向量取反。

        -----

        :param bool inplace: 是否就地修改；默认为 True

        :return: 相反向量；就地修改时，返回向量自身
        :rtype: Vector
        """
        if inplace:
            self._x = -self._x
            self._y = -self._y
            self._z = -self._z
            return self
        else:
            return -self

    def __eq__(self, other):
        try:
            if self._dim == 2:
                return len(other) == 2 and self._x == other[0] and self._y == other[1]
            else:
                return len(other) == 3 and self._x == other[0] and self._y == other[1] and self._z == other[2]
        except:
            return False

    def __ne__(self, other):
        return not self == other

    def copy(self):
        """
        返回当前向量的拷贝。

        -----

        :return: 新向量
        :rtype: Vector
        """
        return Vector(self)

    __pos__ = __deepcopy__ = __copy__ = copy

    def __repr__(self):
        if self._dim == 2:
            return "{0}({1}, {2})".format(self.__class__.__name__, *self)
        else:
            return "{0}({1}, {2}, {3})".format(self.__class__.__name__, *self)

    def __str__(self):
        if self._dim == 2:
            return "({0}, {1})".format(*self)
        else:
            return "({0}, {1}, {2})".format(*self)

    def __getitem__(self, i):
        """
        根据索引获取向量分量。

        -----

        :param int i: 索引

        :return: 分量
        :rtype: float

        :raise IndexError: 索引超出范围
        """
        if i == 0:
            return self._x
        if i == 1:
            return self._y
        if i == 2 and self._dim == 3:
            return self._z
        raise IndexError("Vector index out of range")

    def __setitem__(self, i, value):
        """
        根据索引设置向量某个分量的值。

        -----

        :param int i: 索引
        :param float value: 分量的值

        :return: 无
        :rtype: None

        :raise IndexError: 索引超出范围
        """
        if i == 0:
            self._x = value
        elif i == 1:
            self._y = value
        elif i == 2 and self._dim == 3:
            self._z = value
        else:
            raise IndexError("Vector index out of range")

    def __iter__(self):
        yield self._x
        yield self._y
        if self._dim == 3:
            yield self._z

    def __len__(self):
        return self._dim

    def _op(self, other, operator, scalar_only=False):
        op = _OP_MAP[operator]
        dim = self._dim

        if _is_scalar(other):
            if dim == 2:
                return Vector(op(self._x, other), op(self._y, other))
            else:
                return Vector(op(self._x, other), op(self._y, other), op(self._z, other))

        elif not scalar_only:
            try:
                if dim != len(other):
                    raise VectorError("the dimensions of two vectors are mismatched")
                if dim == 2:
                    return Vector(op(self._x, other[0]), op(self._y, other[1]))
                else:
                    return Vector(op(self._x, other[0]), op(self._y, other[1]), op(self._z, other[2]))
            except VectorError:
                raise
            except:
                # 跳转到下方的TypeError
                pass

        raise TypeError(
            "unsupported operand type(s) for %s: 'Vector' and '%s'"
            % (operator, type(other).__name__)
        )

    def _iop(self, other, operator, scalar_only=False):
        op = _OP_MAP[operator]
        dim = self._dim

        if _is_scalar(other):
            self._x = op(self._x, other)
            self._y = op(self._y, other)
            if dim == 3:
                self._z = op(self._z, other)
            return self

        elif not scalar_only:
            try:
                if dim != len(other):
                    raise VectorError("the dimensions of two vectors are mismatched")
                self._x = op(self._x, other[0])
                self._y = op(self._y, other[1])
                if dim == 3:
                    self._z = op(self._z, other[2])
                return self
            except VectorError:
                raise
            except:
                # 跳转到下方的TypeError
                pass

        raise TypeError(
            "unsupported operand type(s) for %s=: 'Vector' and '%s'"
            % (operator, type(other).__name__)
        )

    def __add__(self, other):
        """
        向量加法（返回新向量）。

        与另一向量相加时，结果为对应分量相加，两个向量的维度需一致；与标量相加时，结果为每个分量同时加上该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '+')

    __radd__ = __add__

    def __iadd__(self, other):
        """
        向量加法（就地修改）。

        与另一向量相加时，结果为对应分量相加，两个向量的维度需一致；与标量相加时，结果为每个分量同时加上该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._iop(other, '+')

    def __sub__(self, other):
        """
        向量减法（返回新向量）。

        与另一向量相减时，结果为对应分量相减，两个向量的维度需一致；与标量相减时，结果为每个分量同时减去该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '-')

    def __rsub__(self, other):
        """
        向量减法（返回新向量）。

        与另一向量相减时，结果为对应分量相减，两个向量的维度需一致；与标量相减时，结果为每个分量同时减去该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return -self + other

    def __isub__(self, other):
        """
        向量减法（就地修改）。

        与另一向量相减时，结果为对应分量相减，两个向量的维度需一致；与标量相减时，结果为每个分量同时减去该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._iop(other, '-')

    def __mul__(self, other):
        """
        向量乘法（返回新向量）。

        只允许与标量相乘，结果为每个分量同时乘以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '*', True)

    def __rmul__(self, other):
        """
        向量乘法（返回新向量）。

        只允许与标量相乘，结果为每个分量同时乘以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self * other

    def __imul__(self, other):
        """
        向量乘法（就地修改）。

        只允许与标量相乘，结果为每个分量同时乘以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._iop(other, '*', True)

    def __truediv__(self, other):
        """
        向量除法（返回新向量）。

        只允许与标量相除，结果为每个分量同时除以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '/', True)

    def __itruediv__(self, other):
        """
        向量除法（就地修改）。

        只允许与标量相除，结果为每个分量同时除以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._iop(other, '/', True)

    __div__ = __truediv__
    __idiv__ = __itruediv__

    def __floordiv__(self, other):
        """
        向量除法（向下整除，返回新向量）。

        只允许与标量相除，结果为每个分量同时除以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '//', True)

    def __ifloordiv__(self, other):
        """
        向量除法（向下整除，就地修改）。

        只允许与标量相除，结果为每个分量同时除以该标量。

        -----

        :param float other: 标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._iop(other, '//', True)

    def dot(self, vec=None):
        """
        向量点积。

        若不传入参数，则计算向量与自身的点积，其数值等于向量长度的平方，即：

        >>> vec.dot() == vec.length2
        True

        -----

        :param Vector|tuple[float]|None vec: 另一向量（Vector、tuple）；若不传入该参数，则计算与自身的点积

        :return: 向量点积
        :rtype: float

        :raise VectorError: 两个向量的维度不一致时抛出
        """
        if vec is None:
            return self.length2
        dim = self._dim
        if dim != len(vec):
            raise VectorError("the dimensions of two vectors are mismatched")
        if dim == 2:
            return self._x * vec[0] + self._y * vec[1]
        else:
            return self._x * vec[0] + self._y * vec[1] + self._z * vec[2]

    def cross(self, vec, inplace=True):
        """
        向量叉积。

        说明
        ----

        仅支持三维向量。

        -----

        :param Vector|tuple[float,float,float] vec: 另一向量（Vector、tuple）
        :param bool inplace: 是否就地修改；默认为 True

        :return: 向量叉积；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 当前向量或传入的向量非三维向量时抛出
        """
        if self._dim != 3 or len(vec) != 3:
            raise VectorError("Vector.cross() only supports 3D vectors")
        vx, vy, vz = vec
        _x, _y, _z = self
        x = _y * vz - _z * vy
        y = _z * vx - _x * vz
        z = _x * vy - _y * vx
        if inplace:
            self._x, self._y, self._z = x, y, z
            return self
        else:
            return Vector(x, y, z)

    def project(self, basis, inplace=True):
        """
        计算当前向量在另一向量上的投影。

        -----

        :param Vector|tuple[float] basis: 另一向量
        :param bool inplace: 是否就地修改；默认为 True

        :return: 投影向量；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 两个向量的维度不一致时抛出
        """
        dim = self._dim
        if dim != len(basis):
            raise VectorError("the dimensions of two vectors are mismatched")
        if dim == 2:
            bx, by = basis
            proj_len = (self._x*bx + self._y*by) / (bx**2 + by**2)
            x = bx * proj_len
            y = by * proj_len
            if inplace:
                self._x, self._y = x, y
                return self
            else:
                return Vector(x, y)
        else:
            bx, by, bz = basis
            proj_len = (self._x*bx + self._y*by + self._z*bz) / (bx**2 + by**2 + bz**2)
            x = bx * proj_len
            y = by * proj_len
            z = bz * proj_len
            if inplace:
                self._x, self._y, self._z = x, y, z
                return self
            else:
                return Vector(x, y, z)

    def project_length(self, basis):
        """
        计算当前向量在另一向量上的投影的长度。

        -----

        :param Vector|tuple[float] basis: 另一向量

        :return: 投影长度
        :rtype: float

        :raise VectorError: 两个向量的维度不一致时抛出
        """
        dim = self._dim
        if dim != len(basis):
            raise VectorError("the dimensions of two vectors are mismatched")
        if dim == 2:
            bx, by = basis
            proj_len = (self._x*bx + self._y*by) / (bx**2 + by**2)
        else:
            bx, by, bz = basis
            proj_len = (self._x*bx + self._y*by + self._z*bz) / (bx**2 + by**2 + bz**2)
        return proj_len

    def angle_between(self, vec, ret_cos=False, rad=False):
        """
        计算当前向量与另一向量之间的夹角。

        -----

        :param Vector|tuple[float] vec: 向量
        :param bool ret_cos: 是否返回夹角的 cos 值；默认为 False
        :param bool rad: 是否使用弧度制，仅 ret_cos 为 False 时有效；默认为 False

        :return: 向量夹角
        :rtype: float
        """
        len1 = self.length
        len2 = vec_length(vec)
        cos = self.dot(vec) / (len1 * len2)
        if ret_cos:
            return cos
        cos = max(-1.0, min(1.0, cos)) # 防止浮点误差超出acos定义域[-1, 1]
        angle = acos(cos)
        return angle if rad else degrees(angle)

    def rotate(self, angle, axis, rad=False, inplace=True):
        """
        对向量应用欧拉旋转。

        说明
        ----

        仅支持三维向量。

        -----

        :param float angle: 旋转角度
        :param str axis: 旋转轴，可选值为 "x"、"y"、"z"
        :param bool rad: 旋转角度是否使用弧度制；默认为 False
        :param bool inplace: 是否就地修改；默认为 True

        :return: 旋转后的向量；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 当前向量非三维向量时抛出
        """
        if self._dim != 3:
            raise VectorError("Vector.rotate() only supports 3D vector")
        if not rad:
            angle = radians(angle)

        c, s = cos(angle), sin(angle)
        _x, _y, _z = self
        if axis == "x":
            x = _x
            y = c * _y - s * _z
            z = s * _y + c * _z
        elif axis == "y":
            x = c * _x + s * _z
            y = _y
            z = -s * _x + c * _z
        elif axis == "z":
            x = c * _x - s * _y
            y = s * _x + c * _y
            z = _z
        else:
            x, y, z = _x, _y, _z

        if inplace:
            self._x, self._y, self._z = x, y, z
            return self
        else:
            return Vector(x, y, z)

    def rotate_around(self, u, angle, rad=False, inplace=True):
        """
        将当前向量绕另一向量旋转。

        说明
        ----

        仅支持三维向量。

        -----

        :param Vector|tuple[float,float,float] u: 旋转轴向量
        :param float angle: 旋转角度
        :param bool rad: 旋转角度是否使用弧度制；默认为 False
        :param bool inplace: 是否就地修改；默认为 True

        :return: 旋转后的向量；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 当前向量或旋转轴向量非三维向量，或旋转轴为零向量时抛出
        """
        if self._dim != 3:
            raise VectorError("Vector.rotate_around() only supports 3D vectors")
        u_len = vec_length(u)
        if u_len == 0:
            raise VectorError("the rotation axis vector must be a non-zero vector")

        vx, vy, vz = self
        ux = u[0] / u_len
        uy = u[1] / u_len
        uz = u[2] / u_len

        if not rad:
            angle = radians(angle)
        cos_theta = cos(angle)
        cos_theta_d = 1 - cos_theta
        sin_theta = sin(angle)
        dot = ux * vx + uy * vy + uz * vz
        cross_x = uy * vz - uz * vy
        cross_y = uz * vx - ux * vz
        cross_z = ux * vy - uy * vx

        x = vx * cos_theta + ux * cos_theta_d * dot + cross_x * sin_theta
        y = vy * cos_theta + uy * cos_theta_d * dot + cross_y * sin_theta
        z = vz * cos_theta + uz * cos_theta_d * dot + cross_z * sin_theta

        if inplace:
            self._x, self._y, self._z = x, y, z
            return self
        else:
            return Vector(x, y, z)


# endregion


# region Functional APIs ===============================================================================================


def dir2rot(direction):
    """
    将方向向量转换为实体头部视角。

    -----

    :param tuple[float,float,float] direction: 方向向量

    :return: 头部视角
    :rtype: tuple[float,float]|None
    """
    if not direction:
        return
    x, y, z = direction
    hori_len = sqrt(x**2 + z**2)
    pitch = degrees(-atan2(y, hori_len))
    yaw = degrees(atan2(-x, z))
    return pitch, yaw


def rot2dir(rot):
    """
    将实体头部视角转换为方向向量。

    -----

    :param tuple[float,float] rot: 头部视角

    :return: 方向向量（单位向量）
    :rtype: tuple[float,float,float]|None
    """
    if not rot:
        return
    pitch = radians(rot[0])
    yaw = radians(rot[1])
    x = -sin(yaw) * cos(pitch)
    y = -sin(pitch)
    z = cos(yaw) * cos(pitch)
    return x, y, z


def dir_from_to(start, end):
    """
    计算由起点指向终点的方向向量。

    -----

    :param tuple[float] start: 起点坐标
    :param tuple[float] end: 终点坐标

    :return: 方向向量（单位向量）
    :rtype: tuple[float]
    """
    vec = vec_sub(end, start)
    return vec_normalize(vec)


def _is_scalar(val):
    return isinstance(val, (float, int))


def vec_length2(vec):
    """
    计算向量长度的平方。

    说明
    ----

    相比于直接计算长度，速度更快。

    -----

    :param tuple[float] vec: 向量

    :return: 向量长度
    :rtype: float
    """
    l = sum(v**2 for v in vec)
    return 0.0 if abs(l) < _ZERO_EPS else l


def vec_length(vec):
    """
    计算向量长度。

    -----

    :param tuple[float] vec: 向量

    :return: 向量长度
    :rtype: float
    """
    return sqrt(vec_length2(vec))


def set_vec_length(vec, length):
    """
    设置向量长度。

    -----

    :param tuple[float] vec: 向量
    :param float length: 长度

    :return: 新向量
    :rtype: tuple[float]

    :raise VectorError: 对零向量调用时抛出
    """
    l = vec_length(vec)
    if l == 0:
        raise VectorError("can't set the length of zero vector")
    return vec_mul(vec, length / l)


def is_zero_vec(vec):
    """
    判断向量是否是零向量。

    -----

    :param tuple[float] vec: 向量

    :return: 是否是零向量
    :rtype: bool
    """
    return all(abs(v) < _ZERO_EPS for v in vec)


def vec_normalize(vec):
    """
    向量标准化。

    -----

    :param tuple[float] vec: 向量

    :return: 标准化向量，长度为1
    :rtype: tuple[float]

    :raise VectorError: 对零向量调用时抛出
    """
    l = vec_length(vec)
    if l == 0:
        raise VectorError("can't normalize zero vector")
    return tuple(v / l for v in vec)


def vec_neg(vec):
    """
    向量取反。

    -----

    :param tuple[float] vec: 向量

    :return: 相反向量
    :rtype: tuple[float]
    """
    return tuple(-v for v in vec)


def vec_add(vec, *more):
    """
    向量加法。

    -----

    :param tuple[float] vec: 向量
    :param tuple[float]|float more: [变长位置参数] 一个或多个向量或标量，按顺序相加

    :return: 结果向量
    :rtype: tuple[float]
    """
    vec = list(vec)
    rng = xrange(len(vec))
    for m in more:
        if _is_scalar(m):
            for i in rng:
                vec[i] += m
        else:
            for i in rng:
                vec[i] += m[i]
    return tuple(vec)


def vec_sub(vec, *more):
    """
    向量减法。

    -----

    :param tuple[float] vec: 向量
    :param tuple[float]|float more: [变长位置参数] 一个或多个向量或标量，按顺序相减

    :return: 结果向量
    :rtype: tuple[float]
    """
    vec = list(vec)
    rng = xrange(len(vec))
    for m in more:
        if _is_scalar(m):
            for i in rng:
                vec[i] -= m
        else:
            for i in rng:
                vec[i] -= m[i]
    return tuple(vec)


def vec_mul(vec, scalar):
    """
    向量与标量相乘。

    -----

    :param tuple[float] vec: 向量
    :param float scalar: 标量

    :return: 结果向量
    :rtype: tuple[float]
    """
    return tuple(v * scalar for v in vec)


def vec_div(vec, scalar):
    """
    向量与标量相除。

    -----

    :param tuple[float] vec: 向量
    :param float scalar: 标量

    :return: 结果向量
    :rtype: tuple[float]
    """
    return tuple(v / scalar for v in vec)


def vec_dot(vec1, vec2):
    """
    向量点积。

    -----

    :param tuple[float] vec1: 向量1
    :param tuple[float] vec2: 向量2

    :return: 向量点积
    :rtype: float
    """
    return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))


def vec_cross(vec1, vec2):
    """
    向量叉积。

    仅支持三维向量。

    -----

    :param tuple[float,float,float] vec1: 向量1
    :param tuple[float,float,float] vec2: 向量2

    :return: 向量叉积
    :rtype: tuple[float,float,float]
    """
    x1, y1, z1 = vec1
    x2, y2, z2 = vec2
    x = y1 * z2 - z1 * y2
    y = z1 * x2 - x1 * z2
    z = x1 * y2 - y1 * x2
    return x, y, z


def vec_project(vec, basis):
    """
    计算向量在另一向量上的投影。

    -----

    :param tuple[float] vec: 向量
    :param tuple[float] basis: 另一向量

    :return: 投影向量
    :rtype: tuple[float]
    """
    proj_len = vec_dot(vec, basis) / vec_length2(basis)
    return vec_mul(basis, proj_len)


def vec_project_length(vec, basis):
    """
    计算当前向量在另一向量上的投影的长度。

    -----

    :param tuple[float] vec: 向量
    :param tuple[float] basis: 另一向量

    :return: 投影长度
    :rtype: float
    """
    return vec_dot(vec, basis) / vec_length2(basis)


def vec_angle_between(vec1, vec2, ret_cos=False, rad=False):
    """
    计算两个向量之间的夹角。

    -----

    :param tuple[float] vec1: 向量1
    :param tuple[float] vec2: 向量2
    :param bool ret_cos: 是否返回夹角的 cos 值；默认为 False
    :param bool rad: 是否使用弧度制，仅 ret_cos 为 False 时有效；默认为 False

    :return: 向量夹角
    :rtype: float
    """
    vec1_len = vec_length(vec1)
    vec2_len = vec_length(vec2)
    cos = vec_dot(vec1, vec2) / (vec1_len * vec2_len)
    if ret_cos:
        return cos
    cos = max(-1.0, min(1.0, cos)) # 防止浮点误差超出acos定义域[-1, 1]
    angle = acos(cos)
    return angle if rad else degrees(angle)


def vec_euler_rotate(vec, x_angle=0.0, y_angle=0.0, z_angle=0.0, order="zyx", rad=False):
    """
    对向量应用欧拉旋转。

    说明
    ----

    仅支持三维向量。

    -----

    :param tuple[float,float,float] vec: 要旋转的向量
    :param float x_angle: 绕x轴的旋转角度；默认为 0.0
    :param float y_angle: 绕y轴的旋转角度；默认为 0.0
    :param float z_angle: 绕z轴的旋转角度；默认为 0.0
    :param str order: 旋转顺序；默认为 "zyx"
    :param bool rad: 旋转角度是否使用弧度制；默认为 False

    :return: 旋转后的向量
    :rtype: tuple[float,float,float]
    """
    if not rad:
        x_angle = radians(x_angle)
        y_angle = radians(y_angle)
        z_angle = radians(z_angle)
    cos_x, sin_x = cos(x_angle), sin(x_angle)
    cos_y, sin_y = cos(y_angle), sin(y_angle)
    cos_z, sin_z = cos(z_angle), sin(z_angle)

    x_matrix = Matrix.Create([
        [1.0, 0.0,   0.0],
        [0.0, cos_x, -sin_x],
        [0.0, sin_x, cos_x],
    ])
    y_matrix = Matrix.Create([
        [cos_y,  0.0, sin_y],
        [0.0,    1.0, 0.0],
        [-sin_y, 0.0, cos_y],
    ])
    z_matrix = Matrix.Create([
        [cos_z, -sin_z, 0.0],
        [sin_z, cos_z,  0.0],
        [0.0,   0.0,    1.0],
    ])

    acc_matrix = Matrix.CreateEye(3)
    for o in order:
        if o == "x":
            acc_matrix *= x_matrix
        elif o == "y":
            acc_matrix *= y_matrix
        elif o == "z":
            acc_matrix *= z_matrix

    column_vec = Matrix.Create([[i] for i in vec])
    res = acc_matrix * column_vec
    return res[0, 0], res[1, 0], res[2, 0]


def vec_rotate_around(v, u, angle, rad=False):
    """
    将向量v绕着向量u旋转。

    说明
    ----

    仅支持三维向量。

    -----

    :param tuple[float,float,float] v: 要旋转的向量
    :param tuple[float,float,float] u: 旋转轴向量
    :param float angle: 旋转角度
    :param bool rad: 旋转角度是否使用弧度制；默认为 False

    :return: 旋转后的向量
    :rtype: tuple[float,float,float]
    """
    u = vec_normalize(u)

    if not rad:
        angle = radians(angle)
    cos_theta = cos(angle)
    sin_theta = sin(angle)
    dot = vec_dot(u, v)
    cross = vec_cross(u, v)

    # v * cos_theta + u * (1 - cos_theta) * dot + cross * sin_theta
    a = vec_mul(v, cos_theta)
    b = vec_mul(u, (1 - cos_theta) * dot)
    c = vec_mul(cross, sin_theta)
    res = vec_add(a, b, c)
    return res


def vec_entity_up(entity_id, ignore_rot_x=False):
    """
    获取实体局部坐标系中朝上的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为 True 时x轴视角将视为 0；默认为 False

    :return: 实体局部坐标系中朝上的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    if ignore_rot_x:
        u = VEC_UP
    else:
        f = vec_entity_forward(entity_id)
        if not f:
            return
        l = vec_normalize(vec_cross(VEC_UP, f))
        u = vec_cross(f, l)
    return u


def vec_entity_down(entity_id, ignore_rot_x=False):
    """
    获取实体局部坐标系中朝下的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为 True 时x轴视角将视为 0；默认为 False

    :return: 实体局部坐标系中朝下的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    if ignore_rot_x:
        d = VEC_DOWN
    else:
        u = vec_entity_up(entity_id)
        if not u:
            return
        d = vec_neg(u)
    return d


def vec_entity_left(entity_id):
    """
    获取实体局部坐标系中朝左的单位向量。

    -----

    :param str entity_id: 实体ID

    :return: 实体局部坐标系中朝左的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    f = vec_entity_forward(entity_id)
    if not f:
        return
    l = vec_normalize(vec_cross(VEC_UP, f))
    return l


def vec_entity_right(entity_id):
    """
    获取实体局部坐标系中朝右的单位向量。

    -----

    :param str entity_id: 实体ID

    :return: 实体局部坐标系中朝右的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    l = vec_entity_left(entity_id)
    if not l:
        return
    r = vec_neg(l)
    return r


def vec_entity_forward(entity_id, ignore_rot_x=False):
    """
    获取实体局部坐标系中朝前的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为 True 时x轴视角将视为 0；默认为 False

    :return: 实体局部坐标系中朝前的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    rot = get_cf(entity_id).Rot.GetRot()
    if not rot:
        return
    if ignore_rot_x:
        rot = (0, rot[1])
    f = rot2dir(rot)
    return f


def vec_entity_backward(entity_id, ignore_rot_x=False):
    """
    获取实体局部坐标系中朝后的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为 True 时x轴视角将视为 0；默认为 False

    :return: 实体局部坐标系中朝后的单位向量，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    f = vec_entity_forward(entity_id, ignore_rot_x)
    if not f:
        return
    b = vec_neg(f)
    return b


def outgoing_vec(vec, normal):
    """
    根据入射向量和法线计算出射向量。

    -----

    :param tuple[float] vec: 入射向量
    :param tuple[float] normal: 法线向量

    :return: 出射向量
    :rtype: tuple[float]
    """
    dot = vec_dot(vec, normal)
    # v - 2 * v.dot(n) * n
    res = vec_sub(vec, vec_mul(normal, 2 * dot))
    return res


# endregion


def __test__():
    from ..core._utils import assert_error
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


def __benchmark__(n, timer, info, **kwargs):
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 0, 1)

    timer.start("Vector+")
    for _ in xrange(n):
        v1 + v2
    timer.end("Vector+")

    timer.start("Vector+=")
    for _ in xrange(n):
        v1 += v2
    timer.end("Vector+=")

    timer.start("Vector-")
    for _ in xrange(n):
        v1 - v2
    timer.end("Vector-")

    timer.start("Vector-=")
    for _ in xrange(n):
        v1 -= v2
    timer.end("Vector-=")

    timer.start("Vector*")
    for _ in xrange(n):
        v1 * 1.0
    timer.end("Vector*")

    timer.start("Vector*=")
    for _ in xrange(n):
        v1 *= 1.0
    timer.end("Vector*=")

    timer.start("Vector/")
    for _ in xrange(n):
        v1 / 1.0
    timer.end("Vector/")

    timer.start("Vector/=")
    for _ in xrange(n):
        v1 /= 1.0
    timer.end("Vector/=")

    timer.start("Vector//")
    for _ in xrange(n):
        v1 // 1.0
    timer.end("Vector//")

    timer.start("Vector//=")
    for _ in xrange(n):
        v1 //= 1.0
    timer.end("Vector//=")

    timer.start("Vector.normalize")
    for _ in xrange(n):
        v1.normalize()
    timer.end("Vector.normalize")

    timer.start("Vector.dot")
    for _ in xrange(n):
        v1.dot(v2)
    timer.end("Vector.dot")

    timer.start("Vector.cross")
    for _ in xrange(n):
        v1.cross(v2)
    timer.end("Vector.cross")

    from mod.common.utils.mcmath import Vector3

    def vec_rotate_around2(v, u, angle):
        v = Vector3(v)
        u = Vector3(u).Normalized()
        angle = radians(angle)
        cos_theta = cos(angle)
        sin_theta = sin(angle)
        dot = Vector3.Dot(u, v)
        cross = Vector3.Cross(u, v)
        res = v * cos_theta + u * (1 - cos_theta) * dot + cross * sin_theta
        return res.ToTuple()

    args = (1.0, 2.0, 3.0), (0.0, 1.0, 0.0), 45.0
    v = Vector(args[0])
    u, angle = args[1:]
    info.append(vec_rotate_around(*args))
    info.append(v.rotate_around(u, angle))
    info.append(vec_rotate_around2(*args))

    timer.start("vec_rotate_around | tuple calc")
    for _ in xrange(n):
        vec_rotate_around(*args)
    timer.end("vec_rotate_around | tuple calc")

    timer.start("vec_rotate_around | nuoyanlib Vector")
    for _ in xrange(n):
        v.rotate_around(u, angle)
    timer.end("vec_rotate_around | nuoyanlib Vector")

    timer.start("vec_rotate_around | modsdk Vector3")
    for _ in xrange(n):
        vec_rotate_around2(*args)
    timer.end("vec_rotate_around | modsdk Vector3")





















