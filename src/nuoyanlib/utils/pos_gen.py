# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


import math


__all__ = [
    "gen_line_pos",
    "gen_circle_pos",
    "gen_sphere_pos",
    "gen_cube_pos",
    "gen_spiral_pos",
]


class _PosGenerator(object):
    def __init__(self, *args, **kwargs):
        self.__i = 0
        self.len = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__i >= self.len:
            self.__i = 0
            raise StopIteration
        pos = self.__gen_pos__(self.__i)
        self.__i += 1
        return pos

    next = __next__

    def __len__(self):
        return self.len

    def __gen_pos__(self, i):
        raise NotImplementedError

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise TypeError("%s indices must be integers, not %s" % (type(self).__name__, type(i).__name__))
        if i >= self.len:
            raise IndexError("%s index out of range" % type(self).__name__)
        return self.__gen_pos__(i)


class gen_line_pos(_PosGenerator):
    """
    [迭代器]

    计算给定两点的连线上各点的坐标（包括 ``pos1`` 和 ``pos2`` ）。

    返回一个迭代器，支持使用 ``for`` 或 ``.next()`` 进行遍历、使用下标获取元素、使用 ``len()`` 获取长度。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2
    :param int count: 生成的坐标数量
    :param int only: 只取前only个点，-1表示取所有点，默认为-1
    """

    def __init__(self, pos1, pos2, count, only=-1):
        super(gen_line_pos, self).__init__()
        self.pos1 = pos1
        self.pos2 = pos2
        self.count = count
        self.only = only
        xd = float(pos2[0] - pos1[0])
        yd = float(pos2[1] - pos1[1])
        zd = float(pos2[2] - pos1[2])
        self.__x_step = xd / (count - 1)
        self.__y_step = yd / (count - 1)
        self.__z_step = zd / (count - 1)
        self.len = only if only != -1 else count

    def __gen_pos__(self, i):
        x = self.pos1[0] + self.__x_step * i
        y = self.pos1[1] + self.__y_step * i
        z = self.pos1[2] + self.__z_step * i
        return x, y, z


class gen_circle_pos(_PosGenerator):
    """
    [迭代器]

    生成以某一坐标为圆心的圆上各点的坐标。

    返回一个迭代器，支持使用 ``for`` 或 ``.next()`` 进行遍历、使用下标获取元素、使用 ``len()`` 获取长度。

    -----

    :param tuple[float,float,float] center_pos: 圆心坐标
    :param float radius: 半径
    :param int count: 生成的坐标数量
    """

    def __init__(self, center_pos, radius, count):
        super(gen_circle_pos, self).__init__()
        self.center_pos = center_pos
        self.radius = radius
        self.count = count
        self.len = count
        self.__step = (2 * math.pi) / self.count

    def __gen_pos__(self, i):
        angle = i * self.__step
        x = self.radius * math.sin(angle) + self.center_pos[0]
        y = self.center_pos[1]
        z = self.radius * math.cos(angle) + self.center_pos[2]
        return x, y, z


class gen_sphere_pos(_PosGenerator):
    """
    [迭代器]

    根据球心、半径生成球面上各点的坐标。

    返回一个迭代器，支持使用 ``for`` 或 ``.next()`` 进行遍历、使用下标获取元素、使用 ``len()`` 获取长度。

    -----

    :param tuple[float,float,float] center_pos: 球心坐标
    :param float radius: 半径
    :param int count: 生成的坐标数量
    """

    def __init__(self, center_pos, radius, count):
        super(gen_sphere_pos, self).__init__()
        self.center_pos = center_pos
        self.radius = radius
        self.count = count
        self.len = count

    def __gen_pos__(self, i):
        if self.count == 1:
            theta = 0.0
            phi = 0.0
        else:
            # 使用斐波那契球采样算法生成均匀分布的点
            theta = math.acos(1 - 2.0 * i / (self.count - 1))
            golden_ratio = (math.sqrt(5) + 1) / 2
            # 使用黄金角度避免周期性重叠
            phi = (2 * math.pi * i) / golden_ratio
        x = self.center_pos[0] + self.radius * math.sin(theta) * math.cos(phi)
        y = self.center_pos[1] + self.radius * math.sin(theta) * math.sin(phi)
        z = self.center_pos[2] + self.radius * math.cos(theta)
        return x, y, z


class gen_cube_pos(_PosGenerator):
    """
    [迭代器]

    生成立方体区域内各点的坐标。

    返回一个迭代器，支持使用 ``for`` 或 ``.next()`` 进行遍历、使用下标获取元素、使用 ``len()`` 获取长度。

    -----

    :param tuple[float,float,float] pos1: 立方体对角坐标1
    :param tuple[float,float,float] pos2: 立方体对角坐标2
    :param int count: 生成的坐标数量
    """

    def __init__(self, pos1, pos2, count):
        super(gen_cube_pos, self).__init__()
        self.pos1 = pos1
        self.pos2 = pos2
        self.count = count
        self.__minx, self.__maxx = sorted([pos1[0], pos2[0]])
        self.__miny, self.__maxy = sorted([pos1[1], pos2[1]])
        self.__minz, self.__maxz = sorted([pos1[2], pos2[2]])
        self.__count_x, self.__count_y, self.__count_z = self._calculate_axis_counts(count)
        self.__x_step = float(self.__maxx - self.__minx) / (self.__count_x - 1) if self.__count_x > 1 else 0.0
        self.__y_step = float(self.__maxy - self.__miny) / (self.__count_y - 1) if self.__count_y > 1 else 0.0
        self.__z_step = float(self.__maxz - self.__minz) / (self.__count_z - 1) if self.__count_z > 1 else 0.0
        self.len = self.__count_x * self.__count_y * self.__count_z

    def _calculate_axis_counts(self, count):
        dx = self.__maxx - self.__minx
        dy = self.__maxy - self.__miny
        dz = self.__maxz - self.__minz
        count_x = max(1, round((dx / (dx + dy + dz)) * (count ** (1 / 3.0))))
        count_y = max(1, round((dy / (dx + dy + dz)) * (count ** (1 / 3.0))))
        count_z = max(1, round((dz / (dx + dy + dz)) * (count ** (1 / 3.0))))
        while count_x * count_y * count_z < count:
            if dx <= dy and dx <= dz:
                count_x += 1
            elif dy <= dx and dy <= dz:
                count_y += 1
            else:
                count_z += 1
        return count_x, count_y, count_z

    def __gen_pos__(self, i):
        # todo
        pass


class gen_spiral_pos(_PosGenerator):
    """
    [迭代器]

    生成螺旋轨迹坐标。

    返回一个迭代器，支持使用 ``for`` 或 ``.next()`` 进行遍历、使用下标获取元素、使用 ``len()`` 获取长度。

    -----

    :param tuple[float,float,float] start_pos: 开始坐标
    :param int count: 生成的坐标数量
    """

    def __init__(self, start_pos, count):
        super(gen_spiral_pos, self).__init__()
        self.start_pos = start_pos
        self.count = count
        self.len = count

    def __gen_pos__(self, i):
        axis = 0
        rel_x, rel_y = 0, 0
        init_step = step = 1
        for _i in range(i + 1):
            if _i > 0:
                if axis == 0:
                    rel_x += 1
                elif axis == 1:
                    rel_y -= 1
                elif axis == 2:
                    rel_x -= 1
                else:
                    rel_y += 1
                step -= 1
                if step <= 0:
                    axis = (axis + 1) % 4
                    if axis == 0 or axis == 2:
                        init_step += 1
                    step = init_step
        x = self.start_pos[0] + rel_x
        y = self.start_pos[1]
        z = self.start_pos[2] + rel_y
        return x, y, z


if __name__ == "__main__":
    poses = gen_line_pos((0, 0, 0), (5, 0, 0), 6, only=3)
    print(len(poses))
    for i in poses:
        print(i)
    print(poses[0], poses[1], poses[2])
    for i in poses:
        print(i)
    # poses[3]
    poses[:3]











