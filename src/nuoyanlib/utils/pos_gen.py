# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-30
#  ⠀
# =================================================


from __future__ import division
from math import sin, cos, pi, acos, sqrt
from random import uniform, random, Random
from ..core._utils import parse_indices_generator
from .mc_math import cartesian_coord, box_min_max


if 0:
    from typing import Any


__all__ = [
    "gen_random_even_pos",
    "gen_line_pos",
    "gen_ring_pos",
    "gen_sphere_pos",
    # "gen_box_pos",
    # "gen_box_surface_pos",
    "gen_box_frame_pos",
]


class _PosGenerator(object):
    def __init__(self):
        self.count = 0

    def __iter__(self):
        for i in xrange(self.count):
            yield self.__gen_pos__(i)

    def __len__(self):
        return self.count

    def __gen_pos__(self, i):
        raise NotImplementedError

    def __getitem__(self, item):
        gen = parse_indices_generator(item, self.count, self.__class__, self.__gen_pos__)
        if isinstance(item, slice):
            return gen
        else:
            return next(gen)


class gen_random_even_pos(_PosGenerator):
    """
    在指定坐标周围，生成随机的均匀分布的多个坐标。

    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float]|tuple[float,float] center: 中心坐标
    :param float radius: 生成半径
    :param int count: 生成的坐标数量
    :param bool fixed_x: 是否固定x轴，固定后x轴取值将总是与 center 一致；默认为 False
    :param bool fixed_y: 是否固定y轴，固定后y轴取值将总是与 center 一致；默认为 False
    :param bool fixed_z: 是否固定z轴，固定后z轴取值将总是与 center 一致；使用二维坐标时可忽略该参数；默认为 False
    :param Any|None seed: 随机数种子，相同的种子将始终得到相同的坐标序列；默认为 None
    """

    __slots__ = (
        '_spawned',
        '_uniform',
        '_random',
        'center',
        'radius',
        'count',
        'fixed_x',
        'fixed_y',
        'fixed_z',
    )

    def __init__(self, center, radius, count, fixed_x=False, fixed_y=False, fixed_z=False, seed=None): # noqa
        if count < 0:
            raise ValueError("'count' must be >=0")
        self._spawned = {}
        if seed is not None:
            rand = Random(seed)
            self._uniform = rand.uniform
            self._random = rand.random
        else:
            self._uniform = uniform
            self._random = random
        self.center = center
        self.radius = radius
        self.count = count
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y
        self.fixed_z = fixed_z

    def __gen_pos__(self, i):
        if i in self._spawned:
            return self._spawned[i]

        if len(self.center) == 2:
            cx, cy = self.center
            r = self.radius * self._random()**(1/2)
            theta = self._uniform(0, 2 * pi)
            pos = (
                cx if self.fixed_x else cx + r * cos(theta),
                cy if self.fixed_y else cy + r * sin(theta),
            )
        else:
            cx, cy, cz = self.center
            r = self.radius * self._random()**(1/3)
            theta = self._uniform(0, 2 * pi)
            phi = self._uniform(0, pi)
            pos = (
                cx if self.fixed_x else cx + r * sin(phi) * cos(theta),
                cy if self.fixed_y else cy + r * sin(phi) * sin(theta),
                cz if self.fixed_z else cz + r * cos(phi),
            )

        self._spawned[i] = pos
        return pos


def _gen_line_pos(start, i, x_step=0, y_step=0, z_step=0):
    x = start[0] + x_step * i
    y = start[1] + y_step * i
    if len(start) == 3:
        z = start[2] + z_step * i
        return x, y, z
    else:
        return x, y


class gen_line_pos(_PosGenerator):
    """
    生成线段上各点的坐标（包括起点和终点），每个坐标均匀分布。

    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float]|tuple[float,float] start: 线段起点坐标
    :param tuple[float,float,float]|tuple[float,float] end: 线段终点坐标
    :param int count: 生成的坐标数量
    """

    __slots__ = ('_x_step', '_y_step', '_z_step', 'start', 'end', 'count')

    def __init__(self, start, end, count): # noqa
        if count < 0:
            raise ValueError("'count' must be >=0")
        c = count - 1
        if c > 0:
            self._x_step = (end[0] - start[0]) / c
            self._y_step = (end[1] - start[1]) / c
            if len(start) == 3:
                self._z_step = (end[2] - start[2]) / c
            else:
                self._z_step = 0.0
        else:
            self._x_step = 0.0
            self._y_step = 0.0
            self._z_step = 0.0
        self.start = start
        self.end = end
        self.count = count

    def __gen_pos__(self, i):
        return _gen_line_pos(self.start, i, self._x_step, self._y_step, self._z_step)


class gen_ring_pos(_PosGenerator):
    """
    生成圆环上各点的坐标，每个坐标均匀分布。

    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float]|tuple[float,float] center: 圆心坐标
    :param float radius: 半径
    :param int count: 生成的坐标数量
    :param str axis_dir: 圆环轴的朝向，可选值为 "x"、"y"、"z"，使用二维坐标时可忽略该参数；默认为 "y"
    """

    __slots__ = ('_step', 'center', 'radius', 'count', 'axis_dir')

    def __init__(self, center, radius, count, axis_dir="y"): # noqa
        if count < 0:
            raise ValueError("'count' must be >=0")
        self._step = ((2 * pi) / count) if count > 0 else 0.0
        self.center = center
        self.radius = radius
        self.count = count
        self.axis_dir = axis_dir

    def __gen_pos__(self, i):
        center = self.center
        radius = self.radius
        axis_dir = self.axis_dir
        theta = i * self._step
        polar = (radius, theta)
        if len(center) == 2:
            return cartesian_coord(polar, True, center)
        else:
            cx, cy, cz = center
            if axis_dir == "x":
                x = cx
                y, z = cartesian_coord(polar, True, (cy, cz))
            elif axis_dir == "y":
                y = cy
                x, z = cartesian_coord(polar, True, (cx, cz))
            else:
                z = cz
                x, y = cartesian_coord(polar, True, (cx, cy))
            return x, y, z


_GOLDEN_RATIO = (sqrt(5) + 1) / 2


class gen_sphere_pos(_PosGenerator):
    """
    生成球面上各点的坐标，每个坐标均匀分布。

    仅支持三维坐标。
    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float] center: 球心坐标
    :param float radius: 半径
    :param int count: 生成的坐标数量
    :param bool fixed_x: 是否固定x轴，固定后x轴取值将总是与 center 一致；默认为 False
    :param bool fixed_y: 是否固定y轴，固定后y轴取值将总是与 center 一致；默认为 False
    :param bool fixed_z: 是否固定z轴，固定后z轴取值将总是与 center 一致；默认为 False
    """

    __slots__ = ('_fixed_count', 'center', 'radius', 'count', 'fixed_x', 'fixed_y', 'fixed_z')

    def __init__(self, center, radius, count, fixed_x=False, fixed_y=False, fixed_z=False): # noqa
        if count < 0:
            raise ValueError("'count' must be >=0")
        self._fixed_count = fixed_x + fixed_y + fixed_z
        self.center = center
        self.radius = radius
        self.count = count
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y
        self.fixed_z = fixed_z

    def __gen_pos__(self, i):
        cx, cy, cz = self.center
        radius = self.radius
        fixed_count = self._fixed_count
        count = self.count

        if fixed_count == 3:
            # 固定三个轴时始终返回中心点
            return self.center

        elif fixed_count == 2:
            # 固定两个轴时退化为线段
            step = (2 * radius / (count - 1)) if count > 1 else 0
            if not self.fixed_x:
                return _gen_line_pos((cx - radius, cy, cz), i, x_step=step)
            elif not self.fixed_y:
                return _gen_line_pos((cx, cy - radius, cz), i, y_step=step)
            else:
                return _gen_line_pos((cx, cy, cz - radius), i, z_step=step)

        elif fixed_count == 1:
            # 固定一个轴时退化为圆盘
            r = radius * (i / count)**0.5
            theta = (2 * pi * i) / _GOLDEN_RATIO
            if self.fixed_x:
                x = cx
                y, z = cartesian_coord((r, theta), True, (cy, cz))
            elif self.fixed_y:
                y = cy
                x, z = cartesian_coord((r, theta), True, (cx, cz))
            else:
                z = cz
                x, y = cartesian_coord((r, theta), True, (cx, cy))
            return x, y, z

        else:
            # 斐波那契球采样算法
            if count > 1:
                theta = acos(1 - 2 * i / (count - 1))
                phi = (2 * pi * i) / _GOLDEN_RATIO
            else:
                theta = phi = 0
            return cartesian_coord((radius, theta, phi), True, (cx, cy, cz))


def _calc_axis_counts(min_pos, max_pos, count):
    dx = max_pos[0] - min_pos[0]
    dy = max_pos[1] - min_pos[1]

    if len(min_pos) == 2:
        ratio = dx / dy if dy > 0 else 1.0
        count_y = max(1, int(round((count / ratio)**0.5)))
        count_x = max(1, int(round(count / count_y)))
        while count_x * count_y < count:
            if count_x / dx < count_y / dy:
                count_x += 1
            else:
                count_y += 1
        return count_x, count_y

    else:
        dz = max_pos[2] - min_pos[2]
        total = dx + dy + dz
        if total == 0:
            return 1, 1, 1
        cube_root = count ** (1/3)
        count_x = max(1, int(round(cube_root * dx / total)))
        count_y = max(1, int(round(cube_root * dy / total)))
        count_z = max(1, int(round(cube_root * dz / total)))
        while count_x * count_y * count_z < count:
            density_x = count_x / dx if dx > 0 else float('inf')
            density_y = count_y / dy if dy > 0 else float('inf')
            density_z = count_z / dz if dz > 0 else float('inf')
            if density_x <= density_y and density_x <= density_z:
                count_x += 1
            elif density_y <= density_z:
                count_y += 1
            else:
                count_z += 1
        return count_x, count_y, count_z


class gen_box_pos(_PosGenerator):
    """
    生成包围盒（立方体/矩形）内各点的坐标，每个坐标均匀分布。

    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 包围盒对角坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 包围盒对角坐标2
    :param int count: 生成的坐标数量
    :param bool allow_exceed: 是否允许实际生成的坐标数量超过 count；默认为 True
    """

    __slots__ = (
        '_min_pos',
        '_count_x',
        '_count_y',
        '_x_step',
        '_y_step',
        '_z_step',
        'pos1',
        'pos2',
        'count',
        'allow_exceed',
    )

    def __init__(self, pos1, pos2, count, allow_exceed=True): # noqa
        min_pos, max_pos = box_min_max(pos1, pos2)
        self._min_pos = min_pos
        if len(pos1) == 2:
            count_x, count_y = _calc_axis_counts(min_pos, max_pos, count)
            count_z = 0
            self._count_x, self._count_y = count_x, count_y
        else:
            count_x, count_y, count_z = _calc_axis_counts(min_pos, max_pos, count)
            self._count_x, self._count_y = count_x, count_y
        self._x_step = ((max_pos[0] - min_pos[0]) / (count_x - 1)) if count_x > 1 else 0.0
        self._y_step = ((max_pos[1] - min_pos[1]) / (count_y - 1)) if count_y > 1 else 0.0
        self._z_step = ((max_pos[2] - min_pos[2]) / (count_z - 1)) if count_z > 1 else 0.0
        self.pos1 = pos1
        self.pos2 = pos2
        self.count = count_x * count_y * count_z if allow_exceed else count
        self.allow_exceed = allow_exceed

    def __gen_pos__(self, i):
        min_pos = self._min_pos
        count_x = self._count_x
        count_y = self._count_y

        if len(self.pos1) == 2:
            ix = i % count_x
            iy = i // count_x
            return (
                min_pos[0] + ix * self._x_step,
                min_pos[1] + iy * self._y_step,
            )

        else:
            ix = i % count_x
            iy = (i // count_x) % count_y
            iz = i // (count_x * count_y)
            return (
                min_pos[0] + ix * self._x_step,
                min_pos[1] + iy * self._y_step,
                min_pos[2] + iz * self._z_step,
            )


class gen_box_surface_pos(_PosGenerator):
    """
    生成包围盒（立方体）表面上各点的坐标，每个坐标均匀分布。

    仅支持三维坐标。
    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float] pos1: 包围盒对角坐标1
    :param tuple[float,float,float] pos2: 包围盒对角坐标2
    :param int count_x: x轴方向上单条边的坐标数量
    :param int count_y: y轴方向上单条边的坐标数量
    :param int count_z: z轴方向上单条边的坐标数量
    """

    __slots__ = (
        '_min_pos',
        '_step_x',
        '_step_y',
        '_step_z',
        'pos1',
        'pos2',
        'count_x',
        'count_y',
        'count_z',
        'count',
    )

    def __init__(self, pos1, pos2, count_x, count_y, count_z): # noqa
        if count_x <= 1:
            raise ValueError("'count_x' must be >1")
        if count_y <= 1:
            raise ValueError("'count_y' must be >1")
        if count_z <= 1:
            raise ValueError("'count_z' must be >1")
        self._min_pos = box_min_max(pos1, pos2)[0]
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        dz = abs(pos1[2] - pos2[2])
        self._step_x = dx / (count_x - 1) if count_x > 1 else 0.0
        self._step_y = dy / (count_y - 1) if count_y > 1 else 0.0
        self._step_z = dz / (count_z - 1) if count_z > 1 else 0.0
        self.pos1 = pos1
        self.pos2 = pos2
        self.count_x = count_x
        self.count_y = count_y
        self.count_z = count_z
        if len(pos1) == 2:
            self.count = count_x * 2 + (count_y * 2 - 4)
        else:
            self.count = count_x * 4 + (count_y * 4 - 8) + (count_z * 4 - 8)

    def __gen_pos__(self, i):
        # todo
        pass


class gen_box_frame_pos(_PosGenerator):
    """
    生成包围盒（立方体/矩形）框架上各点的坐标，每个坐标均匀分布。

    返回一个坐标序列，支持循环遍历、根据索引（下标或切片）获取坐标、使用 ``len()`` 获取序列长度（坐标数量）。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 包围盒对角坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 包围盒对角坐标2
    :param int count_x: x轴方向上单条边的坐标数量，需大于等于2；默认为2
    :param int count_y: y轴方向上单条边的坐标数量，需大于等于2；默认为2
    :param int count_z: z轴方向上单条边的坐标数量，需大于等于2，使用二维坐标时可忽略该参数；默认为2
    """

    __slots__ = (
        'pos1',
        'pos2',
        'count_x',
        'count_y',
        'count_z',
        'count',
        '_vertices',
        '_segments',
        '_dim',
    )

    def __init__(self, pos1, pos2, count_x=2, count_y=2, count_z=2): # noqa
        if pos1 == pos2:
            raise ValueError("'pos1' and 'pos2' cannot be the same")
        if count_x < 2:
            raise ValueError("'count_x' must be >=2")
        if count_y < 2:
            raise ValueError("'count_y' must be >=2")
        if count_z < 2:
            raise ValueError("'count_z' must be >=2")

        self.pos1 = pos1
        self.pos2 = pos2
        self.count_x = count_x
        self.count_y = count_y
        self.count_z = count_z

        self._dim = dim = len(pos1)
        min_pos, max_pos = box_min_max(pos1, pos2)
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        step_x = dx / (count_x - 1)
        step_y = dy / (count_y - 1)

        if dim == 2:
            step_z = 0.0
            min_x, min_y = min_pos
            max_x, max_y = max_pos
            min_z = max_z = None
            self._vertices = list({
                (min_x, min_y),
                (max_x, min_y),
                (min_x, max_y),
                (max_x, max_y),
            })
        else:
            dz = abs(pos1[2] - pos2[2])
            step_z = dz / (count_z - 1)
            min_x, min_y, min_z = min_pos
            max_x, max_y, max_z = max_pos
            self._vertices = list({
                (min_x, min_y, min_z),
                (max_x, min_y, min_z),
                (min_x, min_y, max_z),
                (max_x, min_y, max_z),
                (min_x, max_y, min_z),
                (max_x, max_y, min_z),
                (min_x, max_y, max_z),
                (max_x, max_y, max_z),
            })
        self._vertices.sort()
        self.count = len(self._vertices)

        self._segments = []
        def add_segment(c, start, step):
            c2 = c - 2
            if c2 > 0 and any(s > 0 for s in step):
                self._segments.append((c2, start, step))
                self.count += c2

        x_not_same = (min_x != max_x)
        y_not_same = (min_y != max_y)
        z_not_same = (min_z != max_z)
        if dim == 2:
            step_vec_x = (step_x, 0.0)
            step_vec_y = (0.0, step_y)
            # 下右上左
            add_segment(count_x, (min_x, min_y), step_vec_x)
            if x_not_same:
                add_segment(count_y, (max_x, min_y), step_vec_y)
            if y_not_same:
                add_segment(count_x, (min_x, max_y), step_vec_x)
            add_segment(count_y, (min_x, min_y), step_vec_y)
        else:
            step_vec_x = (step_x, 0.0, 0.0)
            step_vec_y = (0.0, step_y, 0.0)
            step_vec_z = (0.0, 0.0, step_z)
            # 底面
            add_segment(count_x, (min_x, min_y, min_z), step_vec_x)
            if x_not_same:
                add_segment(count_z, (max_x, min_y, min_z), step_vec_z)
            if z_not_same:
                add_segment(count_x, (min_x, min_y, max_z), step_vec_x)
            add_segment(count_z, (min_x, min_y, min_z), step_vec_z)
            # 顶面
            if y_not_same:
                add_segment(count_x, (min_x, max_y, min_z), step_vec_x)
            if x_not_same and y_not_same:
                add_segment(count_z, (max_x, max_y, min_z), step_vec_z)
            if y_not_same and z_not_same:
                add_segment(count_x, (min_x, max_y, max_z), step_vec_x)
            if y_not_same:
                add_segment(count_z, (min_x, max_y, min_z), step_vec_z)
            # 四条竖边
            add_segment(count_y, (min_x, min_y, min_z), step_vec_y)
            if x_not_same:
                add_segment(count_y, (max_x, min_y, min_z), step_vec_y)
            if x_not_same and z_not_same:
                add_segment(count_y, (max_x, min_y, max_z), step_vec_y)
            if z_not_same:
                add_segment(count_y, (min_x, min_y, max_z), step_vec_y)

    def __gen_pos__(self, i):
        # 优先返回顶点
        vn = len(self._vertices)
        if i < vn:
            return self._vertices[i]
        i -= vn

        for seg in self._segments:
            c = seg[0]
            if i < c:
                k = i + 1
                if self._dim == 2:
                    x, y = seg[1]
                    step_x, step_y = seg[2]
                    return (
                        x + step_x * k,
                        y + step_y * k
                    )
                else:
                    x, y, z = seg[1]
                    step_x, step_y, step_z = seg[2]
                    return (
                        x + step_x * k,
                        y + step_y * k,
                        z + step_z * k
                    )

            i -= c

















