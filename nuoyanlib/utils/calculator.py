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
#   Last Modified : 2025-01-09
#
# ====================================================


from math import (
    atan as _atan,
    degrees as _degrees,
    atan2 as _atan2,
    sqrt as _sqrt,
    pi as _pi,
    sin as _sin,
    cos as _cos,
    floor as _floor,
    radians as _radians,
)
from random import (
    randint as _randint,
    uniform as _uniform,
)
from mod.common.utils.mcmath import Vector3 as _Vector3
from mod.common.minecraftEnum import Facing as _Facing
from .._core._sys import (
    get_api as _get_api,
    get_comp_factory as _get_comp_factory,
    LEVEL_ID as _LEVEL_ID,
)


__all__ = [
    "pos_block_facing",
    "to_polar_coordinate",
    "to_cartesian_coordinate",
    "probability_true_i",
    "probability_true_f",
    "pos_distance_to_line",
    "pos_floor",
    "pos_distance",
    "to_relative_pos",
    "to_screen_pos",
    "pos_rotate",
    "straight_pos_list",
    "midpoint",
    "camera_rot_p2p",
    "circle_pos_list",
    "pos_entity_facing",
    "pos_forward_rot",
    "n_quantiles_index_list",
    "cube_center",
    "cube_longest_side_len",
    "is_in_sector",
    "sphere_pos_list",
    "cube_pos_list",
    "spiral_pos_list",
    "is_in_cube",
    "rot_diff",
    "ray_aabb_intersection",
]


def pos_block_facing(pos, face=_Facing.North, dist=1.0):
    """
    | 计算方块某个面朝向的坐标。

    -----

    :param tuple[float,float,float] pos: 方块的坐标
    :param int face: 方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_，默认为Facing.North
    :param float dist: 距离，默认为1.0

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not pos:
        return
    pos = map(float, pos)
    if face == _Facing.Up:
        return pos[0], pos[1] + dist, pos[2]
    elif face == _Facing.Down:
        return pos[0], pos[1] - dist, pos[2]
    elif face == _Facing.East:
        return pos[0] + dist, pos[1], pos[2]
    elif face == _Facing.West:
        return pos[0] - dist, pos[1], pos[2]
    elif face == _Facing.South:
        return pos[0], pos[1], pos[2] + dist
    elif face == _Facing.North:
        return pos[0], pos[1], pos[2] - dist


def to_polar_coordinate(coordinate, rad=False, origin=(0, 0)):
    """
    | 将平面直角坐标转换为极坐标。

    -----

    :param tuple[float,float] coordinate: 平面直角坐标
    :param bool rad: 是否使用弧度制，为False时使用角度制，默认为False
    :param tuple[float,float] origin: 指定坐标原点，默认为(0, 0)

    :return: 极坐标
    :rtype: tuple[float,float]
    """
    x, y = coordinate
    x -= origin[0]
    y -= origin[1]
    r = _sqrt(x ** 2 + y ** 2)
    theta = _atan2(y, x)
    if not rad:
        theta = _degrees(theta)
    return r, theta


def to_cartesian_coordinate(coordinate, rad=False, origin=(0, 0)):
    """
    | 将极坐标转换为平面直角坐标。

    -----

    :param tuple[float,float] coordinate: 极坐标
    :param bool rad: 是否使用弧度制，为False时使用角度制，默认为False
    :param tuple[float,float] origin: 指定坐标原点，默认为(0, 0)

    :return: 平面直角坐标
    :rtype: tuple[float,float]
    """
    r, theta = coordinate
    if not rad:
        theta = _radians(theta)
    x = r * _cos(theta) + origin[0]
    y = r * _sin(theta) + origin[1]
    return x, y


def probability_true_i(n, d):
    """
    | 以指定概率返回 ``True`` 。（分数版本）

    -----

    :param int n: 概率分子
    :param int d: 概率分母

    :return: 以a/b的概率返回True
    :rtype: bool
    """
    return n * d > 0 and _randint(1, d) <= n


def probability_true_f(f):
    """
    | 以指定概率返回 ``True`` 。（浮点数版本）

    -----

    :param float f: 概率，范围为[0, 1]

    :return: 以f的概率返回True
    :rtype: bool
    """
    return f > 0 and _uniform(0, 1) <= f


def pos_distance_to_line(pos, line_pos1, line_pos2):
    """
    | 计算指定坐标 ``pos`` 与指定直线的距离。

    -----

    :param tuple[float,float,float] pos: 指定坐标
    :param tuple[float,float,float] line_pos1: 指定直线上的坐标1
    :param tuple[float,float,float] line_pos2: 指定直线上的坐标2
        
    :return: pos与指定直线的距离
    :rtype: float
    """
    a = pos_distance(pos, line_pos1)
    b = pos_distance(pos, line_pos2)
    c = pos_distance(line_pos1, line_pos2)
    p = (a + b + c) / 2
    s = _sqrt(p * (p - a) * (p - b) * (p - c)) # 海伦公式
    h = s / c * 2
    return h


def pos_floor(pos):
    """
    | 对坐标进行向下取整。

    -----

    :param tuple[float,float,float] pos: 坐标

    :return: 取整后的坐标
    :rtype: tuple[int,int,int]
    """
    return tuple(int(_floor(i)) for i in pos)


def pos_distance(first_point, second_point):
    """
    | 计算两个坐标间的距离。支持多元坐标。

    -----

    :param tuple[float] first_point: 坐标1
    :param tuple[float] second_point: 坐标2
        
    :return: 距离
    :rtype: float
    """
    if not first_point or not second_point:
        return -1.0
    return _sqrt(sum((a - b) ** 2 for a, b in zip(first_point, second_point)))


def to_relative_pos(entity_pos1, entity_pos2):
    """
    | 将实体1的绝对坐标转换为相对实体2的坐标。
        
    -----
    
    :param tuple[float,float,float] entity_pos1: 实体1坐标
    :param tuple[float,float,float] entity_pos2: 实体2坐标
        
    :return: 相对坐标
    :rtype: tuple[float,float,float]|None
    """
    if not entity_pos1 or not entity_pos2:
        return
    return tuple(a - b for a, b in zip(entity_pos1, entity_pos2))


def to_screen_pos(entity_pos, center_pos, screen_size, max_distance, ui_size, player_rot):
    """
    | 将实体的世界坐标转换为屏幕上的平面坐标，并根据玩家水平视角做对应旋转。可用于在小地图上显示实体图标。
        
    -----
    
    :param tuple[float,float,float] entity_pos: 实体坐标
    :param tuple[float,float,float] center_pos: 屏幕坐标系原点对应的世界坐标（一般为玩家坐标）
    :param int screen_size: 屏幕上用于显示实体位置的正方形区域的边长（如小地图的尺寸）
    :param int max_distance: 当实体位于上述区域的边界时，实体与center_pos之间的距离（如小地图的最远绘制距离）
    :param int ui_size: 实体图标ui尺寸
    :param float player_rot: 玩家水平视角
        
    :return: 屏幕坐标
    :rtype: tuple[float,float]|None
    """
    if not entity_pos or not center_pos or not player_rot:
        return
    relative_pos = to_relative_pos(center_pos, entity_pos)
    half_screen_size = screen_size / 2.0
    half_ui_size = ui_size / 2.0
    ratio = (relative_pos[0] / max_distance, relative_pos[2] / max_distance)
    orig_pos = (half_screen_size * ratio[0], half_screen_size * ratio[1])
    rotated_pos = pos_rotate(player_rot, orig_pos)
    screen_pos = (
        half_screen_size - rotated_pos[0] - half_ui_size,
        half_screen_size - rotated_pos[1] - half_ui_size,
    )
    return screen_pos


def pos_rotate(angle, pos):
    """
    | 计算给定坐标绕坐标原点旋转后的新坐标。
        
    -----
    
    :param float angle: 旋转角
    :param tuple[float,float] pos: 原始坐标（二维坐标）
        
    :return: 旋转后的坐标
    :rtype: tuple[float,float]|None
    """
    if not angle or not pos:
        return
    radian = (-angle / 180) * _pi
    rotate_x = _cos(radian) * pos[0] - _sin(radian) * pos[1]
    rotate_y = _cos(radian) * pos[1] + _sin(radian) * pos[0]
    return rotate_x, rotate_y


def straight_pos_list(pos1, pos2, count, only=-1):
    """
    | 计算给定两点连线上各点的坐标（不包括 ``pos1`` 和 ``pos2`` ）。
        
    -----
    
    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2
    :param int count: 返回的坐标的个数
    :param int only: 只取前only个点，-1表示取所有点
        
    :return: 坐标元组列表
    :rtype: list[tuple[float,float,float]]
    """
    if not pos1 or not pos2:
        return []
    xd = pos1[0] - pos2[0]
    yd = pos1[1] - pos2[1]
    zd = pos1[2] - pos2[2]
    x_step = xd / (count + 1)
    y_step = yd / (count + 1)
    z_step = zd / (count + 1)
    result = []
    if only != -1:
        count = only
    while count > 0:
        result.append((pos2[0] + x_step * count, pos2[1] + y_step * count, pos2[2] + z_step * count))
        count -= 1
    return result


def midpoint(first_point, second_point):
    """
    | 计算给定两点间的中点坐标。
        
    -----
    
    :param tuple[float] first_point: 坐标1
    :param tuple[float] second_point: 坐标2
        
    :return: 中点坐标
    :rtype: tuple[float]|None
    """
    if not first_point or not second_point:
        return
    return tuple((a + b) / 2.0 for a, b in zip(first_point, second_point))


def camera_rot_p2p(pos1, pos2):
    """
    | 计算从 ``pos1`` 指向 ``pos2`` 的相机角度。（可用于将玩家相机视角锁定到某一坐标）

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: (竖直角度, 水平角度)
    :rtype: tuple[float,float]|None
    """
    if not pos1 or not pos2:
        return
    x = pos2[0] - pos1[0]
    if x == 0:
        x = 0.000000001
    y = pos2[1] - pos1[1]
    z = pos2[2] - pos1[2]
    hori_dis = pos_distance((pos2[0], pos2[2]), (pos1[0], pos1[2]))
    if hori_dis == 0:
        hori_dis = 0.000000001
    horizontal_rot = 90 + (_atan(z / x) / _pi) * 180 + (0 if x > 0 else -180)
    vertical_rot = -(_atan(y / hori_dis) / _pi) * 180
    return vertical_rot, horizontal_rot


def circle_pos_list(center_pos, radius, density):
    """
    | 计算以某一坐标为圆心的圆上各点的坐标。

    -----

    :param tuple[float,float,float] center_pos: 圆心坐标
    :param float radius: 半径
    :param int density: 返回的坐标个数

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    if not center_pos:
        return []
    result = []
    step = (2 * _pi) / density
    ox, oy, oz = center_pos
    for i in range(density):
        angle = i * step
        nx = radius * _sin(angle) + ox
        nz = radius * _cos(angle) + oz
        result.append((nx, oy, nz))
    return result


def pos_entity_facing(entity_id, dis, use_0yaw=False, height_offset=0.0):
    """
    | 计算实体视角方向上、给定距离上的位置的坐标。

    -----

    :param str entity_id: 实体ID
    :param float dis: 距离
    :param bool use_0yaw: 是否使用0作为实体竖直方向上的视角
    :param float height_offset: 高度偏移量（如实体为玩家建议使用1.6，其他实体建议使用其头部到脚底的距离）

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    comp_factory = _get_comp_factory()
    rot = comp_factory.CreateRot(entity_id).GetRot()
    if not rot:
        return
    if use_0yaw:
        rot = (0, rot[1])
    dir_rot = _get_api().GetDirFromRot(rot)
    ep = comp_factory.CreatePos(entity_id).GetFootPos()
    if not ep:
        return
    ep = (ep[0], ep[1] + height_offset, ep[2])
    result = tuple(ep[i] + dir_rot[i] * dis for i in range(3))
    return result


def pos_forward_rot(pos, rot, dis):
    """
    | 计算从 ``pos`` 射出，以 ``rot`` 为方向的射线上，与 ``pos`` 的距离为 ``dis`` 的位置的坐标。

    -----

    :param tuple[float,float,float] pos: 坐标
    :param tuple[float,float] rot: (竖直角度, 水平角度)
    :param float dis: 距离

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not rot or not pos:
        return
    dir_rot = _get_api().GetDirFromRot(rot)
    result_pos = tuple(pos[i] + dir_rot[i] * dis for i in range(3))
    return result_pos


def n_quantiles_index_list(n, data):
    """
    | 计算一串数据的n分位数的位置。

    -----

    :param int n: n分位
    :param tuple|list|set data: 元组、列表或集合

    :return: n分位数的位置列表
    :rtype: list[int]
    """
    length = len(data)
    result = []
    step = length / n + 1
    index = -1
    while index + step < length - 1:
        index += step
        result.append(index)
    return result


def cube_center(start_pos, end_pos):
    """
    | 计算立方体中心坐标。

    -----

    :param tuple[float,float,float] start_pos: 立方体对角顶点坐标1
    :param tuple[float,float,float] end_pos: 立方体对角顶点坐标2

    :return: 中心坐标
    :rtype: tuple[float,float,float]|None
    """
    if not start_pos or not end_pos:
        return
    x = (start_pos[0] + end_pos[0]) / 2.0
    y = (start_pos[1] + end_pos[1]) / 2.0
    z = (start_pos[2] + end_pos[2]) / 2.0
    return x, y, z


def cube_longest_side_len(start_pos, end_pos):
    """
    | 计算立方体最大棱长。
        
    -----
    
    :param tuple[float,float,float] start_pos: 立方体对角顶点坐标1
    :param tuple[float,float,float] end_pos: 立方体对角顶点坐标2
        
    :return: 最大棱长
    :rtype: float
    """
    if not start_pos or not end_pos:
        return -1.0
    xl = abs(start_pos[0] - end_pos[0])
    yl = abs(start_pos[1] - end_pos[1])
    zl = abs(start_pos[2] - end_pos[2])
    return max(xl, yl, zl)


def is_in_sector(test_pos, vertex_pos, radius, sector_angle, sector_bisector_angle):
    """
    | 判断给定坐标是否在扇形区域内。

    -----
    
    :param tuple[float,float,float] test_pos: 待测试的坐标
    :param tuple[float,float,float] vertex_pos: 扇形顶点坐标
    :param float radius: 扇形半径
    :param float sector_angle: 扇形张开的角度(<=180)
    :param float sector_bisector_angle: 扇形角平分线所在直线的水平角度
        
    :return: 在扇形区域内则返回True，否则返回False
    :rtype: bool
    """
    dis = pos_distance(vertex_pos, test_pos)
    if dis <= radius:
        if sector_angle > 180:
            sector_angle = 180
        elif sector_angle < 0:
            sector_angle = 0
        dx = test_pos[0] - vertex_pos[0]
        dz = test_pos[2] - vertex_pos[2]
        test_pos_angle = -_degrees(_atan2(dx, dz))
        min_angle = sector_bisector_angle - sector_angle / 2
        max_angle = sector_bisector_angle + sector_angle / 2
        range_list = []
        if sector_bisector_angle < 0:
            if min_angle < -180:
                range_list.append((-180, max_angle))
                range_list.append((360 - abs(min_angle), 180))
            else:
                range_list.append((min_angle, max_angle))
        else:
            if max_angle > 180:
                range_list.append((min_angle, 180))
                range_list.append((-180, -360 + max_angle))
            else:
                range_list.append((min_angle, max_angle))
        for r in range_list:
            if r[0] <= test_pos_angle <= r[1]:
                return True
    return False


def sphere_pos_list(center_pos, radius, density):
    """
    | 根据球心、半径计算球面上各点的坐标。
        
    -----
    
    :param tuple[float,float,float] center_pos: 球心坐标
    :param float radius: 半径
    :param int density: 返回的坐标个数
        
    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    step1 = _pi / density
    step2 = (2 * _pi) / density
    a, b = 0, 0
    result = []
    while a < _pi:
        while b < 2 * _pi:
            x = center_pos[0] + radius * _sin(a) * _cos(b)
            y = center_pos[1] + radius * _sin(a) * _sin(b)
            z = center_pos[2] + radius * _cos(a)
            result.append((x, y, z))
            b += step2
        a += step1
        b = 0
    return result


def cube_pos_list(pos1, pos2, step=1):
    """
    | 计算立方体区域内各点的坐标。
        
    -----
    
    :param tuple[float,float,float] pos1: 立方体对角坐标1
    :param tuple[float,float,float] pos2: 立方体对角坐标2
    :param int step: 迭代步长
        
    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    if not pos1 or not pos2 or step <= 0:
        return []
    if pos1[0] <= pos2[0]:
        minx, maxx = pos1[0], pos2[0]
    else:
        minx, maxx = pos2[0], pos1[0]
    if pos1[1] <= pos2[1]:
        miny, maxy = pos1[1], pos2[1]
    else:
        miny, maxy = pos2[1], pos1[1]
    if pos1[2] <= pos2[2]:
        minz, maxz = pos1[2], pos2[2]
    else:
        minz, maxz = pos2[2], pos1[2]
    x, y, z = minx, miny, minz
    result = []
    while x <= maxx:
        y = miny
        while y <= maxy:
            z = minz
            while z <= maxz:
                result.append((x, y, z))
                z += step
            y += step
        x += step
    return result


def spiral_pos_list(start_pos, iterations):
    """
    | 生成螺旋轨迹坐标列表。

    -----

    :param tuple[float,float,float] start_pos: 开始坐标
    :param int iterations: 迭代次数

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    res = []
    axis = 0
    rel_pos = [0, 0]
    init_step = step = 1
    for i in range(iterations):
        if i > 0:
            if axis == 0:
                rel_pos[0] += 1
            elif axis == 1:
                rel_pos[1] -= 1
            elif axis == 2:
                rel_pos[0] -= 1
            else:
                rel_pos[1] += 1
            step -= 1
            if step <= 0:
                axis = (axis + 1) % 4
                if axis == 0 or axis == 2:
                    init_step += 1
                step = init_step
        res.append((start_pos[0] + rel_pos[0], start_pos[1], start_pos[2] + rel_pos[1]))
    return res


def is_in_cube(obj, pos1, pos2, ignore_y=False):
    """
    | 判断对象是否在立方体区域内。
        
    -----
    
    :param str|tuple[float,float,float] obj: 实体ID或坐标
    :param tuple[float,float,float] pos1: 立方体对角顶点坐标1
    :param tuple[float,float,float] pos2: 立方体对角顶点坐标2
    :param bool ignore_y: 是否忽略Y轴
        
    :return: 在立方体区域内返回True，否则返回False
    :rtype: bool
    """
    if isinstance(obj, str):
        target_pos = _get_comp_factory().CreatePos(obj).GetFootPos()
    else:
        target_pos = obj
    if not target_pos or not pos1 or not pos2:
        return False
    def num_in_range(num, r1, r2):
        return r1 <= num <= r2 or r2 <= num <= r1
    for i in range(3):
        if ignore_y and i == 1:
            continue
        if not num_in_range(target_pos[i], pos1[i], pos2[i]):
            return False
    return True


def rot_diff(r1, r2):
    """
    | 计算两个角度之间的实际差值。
        
    -----
    
    :param float r1: 角度1
    :param float r2: 角度2
        
    :return: 差值（-180~180）
    :rtype: float
    """
    diff = r1 - r2
    if diff < -180:
        diff += 360
    elif diff >= 180:
        diff -= 360
    return diff


def ray_aabb_intersection(ray_start_pos, ray_dir, length, cube_center_pos, cube_size):
    """
    | 从指定位置射出一条射线，计算该射线与指定立方体（AABB）的第一个交点坐标，不相交时返回 ``None`` 。

    -----

    :param tuple[float,float,float] ray_start_pos: 射线起始坐标
    :param tuple[float,float,float] ray_dir: 射线方向向量（单位向量）
    :param float length: 射线长度
    :param tuple[float,float,float] cube_center_pos: 立方体中心坐标
    :param tuple[float,float,float] cube_size: 立方体边长元组，分别对应xyz上的边长

    :return: 射线与立方体的第一个交点坐标，不相交时返回None
    :rtype: tuple[float,float,float]|None
    """
    ray_start_pos = _Vector3(ray_start_pos)
    ray_dir = _Vector3(ray_dir)
    cube_center_pos = _Vector3(cube_center_pos)
    local_start_pos = ray_start_pos - cube_center_pos
    t_min = -float('inf')
    t_max = float('inf')
    for i in range(3):
        if ray_dir[i] == 0.0:
            continue
        t1 = (cube_size[i] / 4.0 - local_start_pos[i]) / ray_dir[i]
        t2 = (-cube_size[i] / 4.0 - local_start_pos[i]) / ray_dir[i]
        t_min = max(t_min, min(t1, t2))
        t_max = min(t_max, max(t1, t2))
    if 0.0 <= t_min <= t_max and t_min <= length:
        return (ray_start_pos + ray_dir * t_min).ToTuple()


def get_blocks_by_ray(start_pos, direction, length, dimension=0, count=0, filter_blocks=None):
    """
    | 从指定位置射出一条射线，获取该射线经过的方块。
    | 返回一个列表，方块按照由近到远的顺序排列，列表每个元素为一个字典，结构如下：
    ::

        {
            "name": str, # 方块ID
            "aux": int, # 方块特殊值
            "pos": Tuple[float, float, float], # 方块坐标
            "intersection": Tuple[float, float, float], # 射线与方块的第一个交点的坐标
        }

    | *算法作者：头脑风暴*
    | *修改：* `诺言Nuoyan <https://gitee.com/charming-lee>`_

    -----

    :param tuple[float,float,float] start_pos: 射线起始坐标
    :param tuple[float,float,float] direction: 射线方向向量
    :param float length: 射线长度
    :param int dimension: 维度ID，默认为0
    :param int count: 获取到多少个方块后停止，默认为0，表示不限制数量
    :param list[str]|None filter_blocks: 过滤的方块ID列表，默认过滤空气

    :return: 射线经过的方块的列表，顺序为由近到远，列表每个元素为一个字典，字典结构请见上方
    :rtype: list[dict[str, str|int|tuple]]
    """
    if filter_blocks is None:
        filter_blocks = ["minecraft:air"]
    t_list = [0]
    for n in range(3):
        s = start_pos[n]
        d = direction[n]
        if d == 0:
            continue
        start = int(_floor(s))
        end = int(_floor(s + d * length))
        step_range = range(start + 1, end + 1) if d > 0 else range(start, end, -1)
        for i in step_range:
            t_list.append((i - s) / d)
    t_list.sort()
    t_list = t_list[:-1]
    comp = _get_comp_factory().CreateBlockInfo(_LEVEL_ID)
    block_list = []
    for t in t_list:
        block_pos = [0, 0, 0]
        intersection = [0, 0, 0]
        for n in range(3):
            pos_val = start_pos[n] + t * direction[n]
            intersection[n] = pos_val
            if pos_val.is_integer() and direction[n] < 0:
                pos_val -= 1
            block_pos[n] = int(_floor(pos_val))
        block_pos = tuple(block_pos)
        block = comp.GetBlockNew(block_pos, dimension)
        if block and block['name'] not in filter_blocks:
            block_list.append({
                'name': block['name'],
                'aux': block['aux'],
                'pos': block_pos,
                'intersection': intersection,
            })
            if len(block_list) >= count > 0:
                break
    return block_list















