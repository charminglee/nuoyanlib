# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-20
#  ⠀
# =================================================


import operator
import math
from mod.common.utils.mcmath import Matrix
from ..core._sys import get_cf, get_api
from ..core.error import VectorError


__all__ = [
    "Vector",
    "is_zero_vec",
    "set_vec_length",
    "vec_orthogonal_decomposition",
    "vec_entity_left",
    "vec_entity_right",
    "vec_entity_forward",
    "vec_entity_backward",
    "vec_entity_up",
    "vec_entity_down",
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


_ZERO_EPS = 1e-9


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

    可传入2个或3个 ``float`` / ``int`` ，也可传入一个包含2个或3个 ``float`` / ``int`` 的 ``tuple`` 。若不传入任何参数，则创建一个三维零向量。

    -----

    :raise VectorError: 传入的参数不合法
    """

    __slots__ = ('_x', '_y', '_z', '_dim')

    def __init__(self, *args):
        l = len(args)
        try:
            if l == 0:
                self._x = self._y = self._z = 0.0
                self._dim = 3
            elif l == 1:
                vec = map(float, args[0])
                if len(vec) == 2:
                    self._x, self._y = vec
                    self._z = 0.0
                    self._dim = 2
                else:
                    self._x, self._y, self._z = map(float, vec)
                    self._dim = 3
            elif l == 2:
                self._x, self._y = map(float, args)
                self._z = 0.0
                self._dim = 2
            elif l == 3:
                self._x, self._y, self._z = map(float, args)
                self._dim = 3
            else:
                raise
        except:
            raise VectorError("invalid Vector construction arguments: {}".format(args))

    @staticmethod
    def zero(is_3d=True):
        """
        [静态方法]

        创建一个零向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: 零向量
        :rtype: Vector
        """
        return Vector(0.0, 0.0, 0.0) if is_3d else Vector(0.0, 0.0)

    @staticmethod
    def one(is_3d=True):
        """
        [静态方法]

        创建一个所有分量均为 ``1.0`` 的向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: 所有分量均为1.0的向量
        :rtype: Vector
        """
        return Vector(1.0, 1.0, 1.0) if is_3d else Vector(1.0, 1.0)

    @staticmethod
    def left(is_3d=True):
        """
        [静态方法]

        创建一个x分量为 ``1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: x分量为1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(1.0, 0.0, 0.0) if is_3d else Vector(1.0, 0.0)

    @staticmethod
    def right(is_3d=True):
        """
        [静态方法]

        创建一个x分量为 ``-1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: x分量为-1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(-1.0, 0.0, 0.0) if is_3d else Vector(-1.0, 0.0)

    @staticmethod
    def up(is_3d=True):
        """
        [静态方法]

        创建一个y分量为 ``1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: y分量为1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(0.0, 1.0, 0.0) if is_3d else Vector(0.0, 1.0)

    @staticmethod
    def down(is_3d=True):
        """
        [静态方法]

        创建一个y分量为 ``-1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :param bool is_3d: 是否返回三维向量

        :return: y分量为1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(0.0, -1.0, 0.0) if is_3d else Vector(0.0, -1.0)

    @staticmethod
    def forward():
        """
        [静态方法]

        创建一个z分量为 ``1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :return: z分量为1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(0.0, 0.0, 1.0)

    @staticmethod
    def backward():
        """
        [静态方法]

        创建一个z分量为 ``-1.0`` ，其余分量为 ``0.0`` 的向量。

        -----

        :return: z分量为-1.0，其余分量为0.0的向量
        :rtype: Vector
        """
        return Vector(0.0, 0.0, -1.0)

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
        self._x = float(val)

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
        self._y = float(val)

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
        self._z = float(val)

    @property
    def xy(self):
        """
        [只读属性]

        返回由向量xy分量组成的元组 ``(x,⠀y)`` 。

        :rtype: tuple[float,float]
        """
        return self._x, self._y

    @property
    def xz(self):
        """
        [只读属性]

        返回由向量xz分量组成的元组 ``(x,⠀z)`` 。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float]
        """
        return self._x, self._z

    @property
    def yz(self):
        """
        [只读属性]

        返回由向量yz分量组成的元组 ``(y,⠀z)`` 。

        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float]
        """
        return self._y, self._z

    @property
    def xyz(self):
        """
        [只读属性]

        返回由向量xyz分量组成的元组 ``(x,⠀y,⠀z)`` 。

        等价于 ``tuple(vec)`` 。
        若向量为二维向量，则z分量为 ``0.0`` 。

        :rtype: tuple[float,float,float]
        """
        return self._x, self._y, self._z

    @property
    def length(self):
        """
        [可读写属性]

        向量长度。

        :rtype: float
        """
        return 0.0 if self.is_zero() else math.sqrt(self.length2)

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

    @property
    def length2(self):
        """
        [只读属性]

        向量长度的平方。

        相比于直接计算长度，速度更快。

        :rtype: float
        """
        return 0.0 if self.is_zero() else (self._x**2 + self._y**2 + self._z**2)

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

        :param bool inplace: 是否就地修改，默认为True

        :return: 标准化向量；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 对零向量调用时抛出
        """
        l = self.length
        if l == 0:
            raise VectorError("can't normalize zero vector")
        mul = 1 / l
        x = self._x * mul
        y = self._y * mul
        z = self._z * mul
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

        :param bool inplace: 是否就地修改，默认为True

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
        return Vector(self._x, self._y) if self._dim == 2 else Vector(self._x, self._y, self._z)

    __deepcopy__ = __copy__ = copy

    def __repr__(self):
        if self._dim == 2:
            return "Vector({}, {})".format(self._x, self._y)
        else:
            return "Vector({}, {}, {})".format(self._x, self._y, self._z)

    def __str__(self):
        if self._dim == 2:
            return "({}, {})".format(self._x, self._y)
        else:
            return "({}, {}, {})".format(self._x, self._y, self._z)

    def __getitem__(self, i):
        """
        获取向量分量。

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
        设置向量某个分量的值。

        -----

        :param int i: 索引
        :param float value: 分量的值

        :return: 无
        :rtype: None

        :raise IndexError: 索引超出范围
        """
        if i == 0:
            self._x = float(value)
        elif i == 1:
            self._y = float(value)
        elif i == 2 and self._dim == 3:
            self._z = float(value)
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

        if isinstance(other, (int, float)):
            if self._dim == 2:
                return Vector(op(self._x, other), op(self._y, other))
            else:
                return Vector(op(self._x, other), op(self._y, other), op(self._z, other))

        elif not scalar_only:
            try:
                if self._dim != len(other):
                    raise VectorError("the dimensions of two vectors are mismatched")
                if self._dim == 2:
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

        if isinstance(other, (int, float)):
            self._x = op(self._x, other)
            self._y = op(self._y, other)
            if self._dim == 3:
                self._z = op(self._z, other)
            return self

        elif not scalar_only:
            try:
                if self._dim != len(other):
                    raise VectorError("the dimensions of two vectors are mismatched")
                self._x = op(self._x, other[0])
                self._y = op(self._y, other[1])
                if self._dim == 3:
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

        :raise VectorDimError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self._op(other, '+')

    def __radd__(self, other):
        """
        向量加法（返回新向量）。

        与另一向量相加时，结果为对应分量相加，两个向量的维度需一致；与标量相加时，结果为每个分量同时加上该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 新向量
        :rtype: Vector

        :raise VectorDimError: 两个向量的维度不一致时抛出
        :raise TypeError: 与不支持的类型进行运算时抛出
        """
        return self + other

    def __iadd__(self, other):
        """
        向量加法（就地修改）。

        与另一向量相加时，结果为对应分量相加，两个向量的维度需一致；与标量相加时，结果为每个分量同时加上该标量。

        -----

        :param Vector|tuple[float]|float other: 另一向量（Vector、tuple）或标量（int、float）

        :return: 向量自身
        :rtype: Vector

        :raise VectorDimError: 两个向量的维度不一致时抛出
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

        :raise VectorDimError: 两个向量的维度不一致时抛出
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

        :raise VectorDimError: 两个向量的维度不一致时抛出
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

        :raise VectorDimError: 两个向量的维度不一致时抛出
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

    def dot(self, vec):
        """
        向量点积。

        -----

        :param Vector|tuple[float] vec: 另一向量（Vector、tuple）

        :return: 向量点积
        :rtype: float

        :raise VectorError: 两个向量的维度不一致时抛出
        """
        if self._dim != len(vec):
            raise VectorError("the dimensions of two vectors are mismatched")
        return sum(self[i] * vec[i] for i in xrange(self._dim))

    def cross(self, vec, inplace=True):
        """
        向量叉积。

        仅支持三维向量。

        -----

        :param Vector|tuple[float,float,float] vec: 另一向量（Vector、tuple）
        :param bool inplace: 是否就地修改，默认为True

        :return: 向量叉积；就地修改时，返回向量自身
        :rtype: Vector

        :raise VectorError: 当前向量非三维向量，或传入非三维向量时抛出
        """
        if self._dim != 3 or len(vec) != 3:
            raise VectorError("cross product only supports 3D vectors")
        x = self._y * vec[2] - self._z * vec[1]
        y = self._z * vec[0] - self._x * vec[2]
        z = self._x * vec[1] - self._y * vec[0]
        if inplace:
            self._x, self._y, self._z = x, y, z
            return self
        else:
            return Vector(x, y, z)


# endregion


# region Functional APIs ===============================================================================================


def is_zero_vec(vec):
    """
    判断向量是否是零向量。

    -----

    :param tuple[float] vec: 向量

    :return: 是否是零向量
    :rtype: bool
    """
    return all(abs(v) < _ZERO_EPS for v in vec)


def set_vec_length(vec, length, ret_vector=False):
    """
    设置向量长度。

    -----

    :param Vector|tuple[float] vec: 向量
    :param float length: 长度
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 向量
    :rtype: Vector|tuple[float]

    :raise ZeroVectorError: 传入零向量时抛出
    """
    vec = _to_vector(vec)
    vec.length = length
    return vec if ret_vector else tuple(vec)


def vec_orthogonal_decomposition(vec, basis1, basis2, ret_vector=False):
    """
    对向量进行正交分解。

    -----

    :param Vector|tuple[float] vec: 要分解的向量
    :param Vector|tuple[float] basis1: 正交基1
    :param Vector|tuple[float] basis2: 正交基2
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 分解后的两个向量，第一个向量沿basis1方向，第二个向量沿basis2方向
    :rtype: tuple[Vector|tuple[float],Vector|tuple[float]]
    """
    vec = _to_vector(vec)
    basis1 = _to_vector(basis1)
    basis2 = _to_vector(basis2)
    vec1 = (vec.dot(basis1) / basis1.dot(basis1)) * basis1
    vec2 = (vec.dot(basis2) / basis2.dot(basis2)) * basis2
    return (vec1, vec2) if ret_vector else (tuple(vec1), tuple(vec2))


def vec_entity_left(entity_id, ret_vector=False):
    """
    获取实体局部坐标系中朝左的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝左的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    f = vec_entity_forward(entity_id, ret_vector=True)
    if not f:
        return None
    l = Vector.up().cross(f).normalize()
    return l if ret_vector else tuple(l)


def vec_entity_right(entity_id, ret_vector=False):
    """
    获取实体局部坐标系中朝右的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝右的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    l = vec_entity_left(entity_id, True)
    if not l:
        return
    r = l.neg()
    return r if ret_vector else tuple(r)


def vec_entity_forward(entity_id, ignore_rot_x=False, ret_vector=False):
    """
    获取实体局部坐标系中朝前的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为True时x轴视角将视为0，默认为False
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝前的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    rot = get_cf(entity_id).Rot.GetRot()
    if not rot:
        return
    if ignore_rot_x:
        rot = (0, rot[1])
    f = get_api().GetDirFromRot(rot)
    return Vector(f) if ret_vector else f


def vec_entity_backward(entity_id, ignore_rot_x=False, ret_vector=False):
    """
    获取实体局部坐标系中朝后的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为True时x轴视角将视为0，默认为False
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝后的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    f = vec_entity_forward(entity_id, ignore_rot_x, True)
    if not f:
        return
    b = f.neg()
    return b if ret_vector else tuple(b)


def vec_entity_up(entity_id, ignore_rot_x=False, ret_vector=False):
    """
    获取实体局部坐标系中朝上的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为True时x轴视角将视为0，默认为False
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝上的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    if ignore_rot_x:
        u = Vector.up()
    else:
        f = vec_entity_forward(entity_id, ret_vector=True)
        if not f:
            return None
        l = Vector.up().cross(f).normalize()
        u = f.cross(l)
    return u if ret_vector else tuple(u)


def vec_entity_down(entity_id, ignore_rot_x=False, ret_vector=False):
    """
    获取实体局部坐标系中朝下的单位向量。

    -----

    :param str entity_id: 实体ID
    :param bool ignore_rot_x: 是否忽略x轴视角，设为True时x轴视角将视为0，默认为False
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 实体局部坐标系中朝下的单位向量，获取失败返回None
    :rtype: Vector|tuple[float,float,float]|None
    """
    if ignore_rot_x:
        d = Vector.down()
    else:
        u = vec_entity_up(entity_id, ret_vector=True)
        if not u:
            return
        d = u.neg()
    return d if ret_vector else tuple(d)


def vec_normalize(vec, ret_vector=False):
    """
    向量标准化。

    -----

    :param Vector|tuple[float] vec: 向量
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 单位向量，长度为1
    :rtype: Vector|tuple[float]

    :raise ZeroVectorError: 传入零向量时抛出
    """
    return set_vec_length(vec, 1, ret_vector)


def vec_rot_p2p(pos1, pos2):
    """
    计算从 ``pos1`` 指向 ``pos2`` 的向量角度。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: 角度元组，分别为竖直角度、水平角度
    :rtype: tuple[float,float]
    """
    from .mc_math import distance
    x = pos2[0] - pos1[0]
    if x == 0:
        x = 0.000000001
    y = pos2[1] - pos1[1]
    z = pos2[2] - pos1[2]
    hori_dis = distance((pos2[0], pos2[2]), (pos1[0], pos1[2]))
    if hori_dis == 0:
        hori_dis = 0.000000001
    horizontal_rot = (math.atan(z / x) / math.pi) * 180
    vertical_rot = (math.atan(y / hori_dis) / math.pi) * 180 * (-1 if x < 0 else 1)
    return vertical_rot, horizontal_rot


def vec_p2p(pos1, pos2, ret_vector=False):
    """
    计算从 ``pos1`` 指向 ``pos2`` 的单位向量。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 从pos1指向pos2的单位向量
    :rtype: Vector|tuple[float,float,float]
    """
    vec = _to_vector(pos2) - _to_vector(pos1)
    vec.normalize()
    return vec if ret_vector else tuple(vec)


def vec_length(vec):
    """
    计算向量长度。

    -----

    :param Vector|tuple[float] vec: 向量

    :return: 向量长度
    :rtype: float
    """
    return _to_vector(vec).length


def vec_angle(vec1, vec2):
    """
    计算两个向量之间的夹角。

    -----

    :param Vector|tuple[float] vec1: 向量1
    :param Vector|tuple[float] vec2: 向量2

    :return: 夹角弧度值
    :rtype: float
    """
    vec1 = _to_vector(vec1)
    vec2 = _to_vector(vec2)
    vec1_len = vec1.length
    vec2_len = vec2.length
    cos = vec1.dot(vec2) / (vec1_len * vec2_len)
    return math.acos(cos)


def vec_euler_rotate(vec, x_angle=0.0, y_angle=0.0, z_angle=0.0, order="zyx", ret_vector=False):
    """
    对指定向量应用欧拉旋转。

    -----

    :param Vector|tuple[float,float,float] vec: 要旋转的向量
    :param float x_angle: 绕x轴的旋转角度（角度制，下同）
    :param float y_angle: 绕y轴的旋转角度
    :param float z_angle: 绕z轴的旋转角度
    :param str order: 旋转顺序，默认为"zyx"，即先按z轴旋转，再按y轴旋转，最后按x轴旋转
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 旋转后的向量
    :rtype: Vector|tuple[float,float,float]
    """
    x_angle = math.radians(x_angle)
    y_angle = math.radians(y_angle)
    z_angle = math.radians(z_angle)
    cos_x, sin_x = math.cos(x_angle), math.sin(x_angle)
    cos_y, sin_y = math.cos(y_angle), math.sin(y_angle)
    cos_z, sin_z = math.cos(z_angle), math.sin(z_angle)

    x_matrix = Matrix.Create([
        [1, 0,     0],
        [0, cos_x, -sin_x],
        [0, sin_x, cos_x],
    ])
    y_matrix = Matrix.Create([
        [cos_y,  0, sin_y],
        [0,      1, 0],
        [-sin_y, 0, cos_y],
    ])
    z_matrix = Matrix.Create([
        [cos_z, -sin_z, 0],
        [sin_z, cos_z,  0],
        [0,     0,      1],
    ])

    acc_matrix = Matrix.CreateEye(3)
    for axis in order:
        if axis == 'x':
            acc_matrix *= x_matrix
        elif axis == 'y':
            acc_matrix *= y_matrix
        elif axis == 'z':
            acc_matrix *= z_matrix

    column_vec = Matrix.Create([[i] for i in vec])
    rotated = acc_matrix * column_vec
    if ret_vector:
        return Vector(rotated[0, 0], rotated[1, 0], rotated[2, 0])
    else:
        return rotated[0, 0], rotated[1, 0], rotated[2, 0]


def vec_rotate_around(v, u, angle, ret_vector=False):
    """
    将向量v绕着向量u旋转。

    :param Vector|tuple[float] v: 要旋转的向量
    :param Vector|tuple[float] u: 旋转轴向量
    :param float angle: 旋转角度
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 旋转后的向量
    :rtype: Vector|tuple[float]
    """
    v = _to_vector(v)
    v_len = v.length
    v.normalize()
    u = _to_vector(u).normalize()
    theta = math.radians(angle)
    cos = math.cos(theta)
    sin = math.sin(theta)
    dot = u.dot(v)
    cross = u.cross(v, False)
    res = v * cos + u * (1 - cos) * dot + cross * sin # 罗德里格旋转公式
    res *= v_len
    return res if ret_vector else tuple(res)


def outgoing_vec(vec, normal, ret_vector=False):
    """
    已知入射向量和法线求出射向量。

    -----

    :param Vector|tuple[float] vec: 入射向量
    :param Vector|tuple[float] normal: 法线向量
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 出射向量
    :rtype: Vector|tuple[float]
    """
    v = _to_vector(vec)
    n = _to_vector(normal)
    reflex_vec = v - 2 * v.dot(n) * n
    return reflex_vec if ret_vector else tuple(reflex_vec)


def vec_composite(ret_vector, vec, *more_vec):
    """
    向量的合成。

    -----

    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple
    :param Vector|tuple[float] vec: 向量
    :param Vector|tuple[float] more_vec: 更多向量

    :return: 合向量
    :rtype: Vector|tuple[float]
    """
    res = _to_vector(vec)
    for v in more_vec:
        res += _to_vector(v)
    return res if ret_vector else tuple(res)


def vec_scale(vec, scale, ret_vector=False):
    """
    向量缩放。

    -----

    :param Vector|tuple[float] vec: 向量
    :param float scale: 缩放倍率
    :param bool ret_vector: 是否以Vector类型返回，默认为False，返回tuple

    :return: 缩放后的向量
    :rtype: Vector|tuple[float]
    """
    res = _to_vector(vec) * scale
    return res if ret_vector else tuple(res)


# endregion


def __test__():
    Vector("NY")
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
























