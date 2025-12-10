# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-11
|
| ====================================================
"""


from math import degrees, atan2, sqrt, pi, sin, cos, floor, radians
from random import uniform
from mod.common.utils.mcmath import Vector3
from mod.common.minecraftEnum import Facing
from ..core._sys import get_comp_factory, get_api, LEVEL_ID
from .vector import Vector


__all__ = [
    "distance2nearest_entity",
    "distance2nearest_player",
    "range_map",
    "to_chunk_pos",
    "to_aabb",
    "pos_distance_square",
    "clamp",
    "pos_block_facing",
    "to_polar_coordinate",
    "to_cartesian_coordinate",
    "probability",
    "pos_distance_to_line",
    "pos_floor",
    "pos_distance",
    "to_relative_pos",
    "to_screen_pos",
    "pos_rotate",
    "midpoint",
    "camera_rot_p2p",
    "pos_entity_facing",
    "pos_forward_rot",
    "n_quantiles_index_list",
    "cube_center",
    "cube_longest_side_len",
    "is_in_cylinder",
    "is_in_sector",
    "is_in_cube",
    "rot_diff",
    "ray_aabb_intersection",
]


def distance2nearest_entity(target):
    """
    获取指定目标与其距离最近的实体的距离。
    
    -----
    
    :param tuple[float,float,float]|str target: 目标，可传入坐标或实体ID
    
    :return: 目标与距离最近的实体的距离，若获取失败，返回-1
    :rtype: float
    """
    tp = CF(target).Pos.GetFootPos() if isinstance(target, str) else target
    if not tp:
        return -1
    min_dist2 = -1
    for entity_id in get_all_entities():
        ep = CF(entity_id).Pos.GetFootPos()
        if not ep:
            continue
        dist2 = pos_distance_square(tp, ep)
        if min_dist2 == -1 or dist2 < min_dist2:
            min_dist2 = dist2
    return sqrt(min_dist2) if min_dist2 != -1 else -1


def distance2nearest_player(target):
    """
    获取指定目标与其距离最近的玩家的距离。
    
    -----
    
    :param tuple[float,float,float]|str target: 目标，可传入坐标或实体ID
    
    :return: 目标与距离最近的玩家的距离，若获取失败，返回-1
    :rtype: float
    """
    tp = CF(target).Pos.GetFootPos() if isinstance(target, str) else target
    if not tp:
        return -1
    player_lst = get_api().GetPlayerList()
    min_dist2 = -1
    for player_id in player_lst:
        pp = CF(player_id).Pos.GetFootPos()
        if not pp:
            continue
        dist2 = pos_distance_square(tp, pp)
        if min_dist2 == -1 or dist2 < min_dist2:
            min_dist2 = dist2
    return sqrt(min_dist2) if min_dist2 != -1 else -1


def range_map(x, output_range, input_range=(0, 1), func=lambda t: t):
    """
    将某个范围内的数值映射到另一个范围。

    -----

    :param float x: 输入值
    :param tuple[float,float] output_range: 输出范围，如 (0, 1)，表示范围0~1
    :param tuple[float,float] input_range: 输入范围，默认为 (0, 1)
    :param function func: 插值函数，接受一个参数 t ∈ [0, 1]，返回 [0, 1] 的值；默认为 lambda t: t，即线性映射

    :return: 映射值
    :rtype: float
    """
    j, k = output_range
    m, n = input_range
    t = float(x - m) / (n - m)
    t = func(t)
    return j + (k - j) * t


def to_chunk_pos(pos):
    """
    将世界坐标转换为所在区块坐标。

    -----

    :param tuple[float,float,float] pos: 世界坐标

    :return: 区块坐标
    :rtype: tuple[int,int]|None
    """
    if not pos:
        return
    pos = pos_floor(pos)
    return int(pos[0] // 16), int(pos[2] // 16)


def to_aabb(pos1, pos2):
    """
    将任意两点坐标转换为以这两点为顶点的长方体区域的最小点和最大点（AABB）。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: 最小点和最大点坐标
    :rtype: tuple[tuple[float,float,float],tuple[float,float,float]]|None
    """
    if not pos1 or not pos2:
        return
    min_pos = (min(pos1[0], pos2[0]), min(pos1[1], pos2[1]), min(pos1[2], pos2[2]))
    max_pos = (max(pos1[0], pos2[0]), max(pos1[1], pos2[1]), max(pos1[2], pos2[2]))
    return min_pos, max_pos


def pos_distance_square(pos1, pos2):
    """
    计算两个坐标间距离的平方，相比于直接计算距离速度更快。

    -----

    :param tuple[float] pos1: 坐标1
    :param tuple[float] pos2: 坐标2

    :return: 坐标距离的平方，若任一坐标为None，返回-1.0
    :rtype: float
    """
    if not pos1 or not pos2:
        return -1.0
    return sum((a - b) ** 2 for a, b in zip(pos1, pos2))


def clamp(x, min_value, max_value):
    """
    将数值限制在指定范围内。

    小于 ``min_value`` 的值将被限制为 ``min_value`` ，大于 ``max_value`` 的值将被限制为 ``max_value`` 。

    -----

    :param float x: 数值
    :param float min_value: 最小值
    :param float max_value: 最大值

    :return: 限制后的值
    :rtype: float
    """
    return max(min_value, min(max_value, x))


def pos_block_facing(pos, face=Facing.North, dist=1.0):
    """
    计算方块某个面朝向的坐标。

    -----

    :param tuple[float,float,float] pos: 方块的坐标
    :param int face: 方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_，默认为Facing.North
    :param float dist: 距离，默认为1.0

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not pos:
        return
    pos = map(float, pos) # type: list[float]
    if face == Facing.Up:
        return pos[0], pos[1] + dist, pos[2]
    elif face == Facing.Down:
        return pos[0], pos[1] - dist, pos[2]
    elif face == Facing.East:
        return pos[0] + dist, pos[1], pos[2]
    elif face == Facing.West:
        return pos[0] - dist, pos[1], pos[2]
    elif face == Facing.South:
        return pos[0], pos[1], pos[2] + dist
    elif face == Facing.North:
        return pos[0], pos[1], pos[2] - dist


def to_polar_coordinate(coordinate, rad=False, origin=(0, 0)):
    """
    将平面直角坐标转换为极坐标。

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
    r = sqrt(x ** 2 + y ** 2)
    theta = atan2(y, x)
    if not rad:
        theta = degrees(theta)
    return r, theta


def to_cartesian_coordinate(coordinate, rad=False, origin=(0, 0)):
    """
    将极坐标转换为平面直角坐标。

    -----

    :param tuple[float,float] coordinate: 极坐标
    :param bool rad: 是否使用弧度制，为False时使用角度制，默认为False
    :param tuple[float,float] origin: 指定坐标原点，默认为(0, 0)

    :return: 平面直角坐标
    :rtype: tuple[float,float]
    """
    r, theta = coordinate
    if not rad:
        theta = radians(theta)
    x = r * cos(theta) + origin[0]
    y = r * sin(theta) + origin[1]
    return x, y


def probability(p):
    """
    以指定概率返回 ``True`` 。

    -----

    :param float p: 概率，范围为[0, 1]

    :return: 以p的概率返回True，否则返回False
    :rtype: bool
    """
    return p > 0 and uniform(0, 1) <= p


def pos_distance_to_line(pos, line_pos1, line_pos2):
    """
    计算指定坐标 ``pos`` 与指定直线的距离。

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
    s = sqrt(p * (p - a) * (p - b) * (p - c)) # 海伦公式
    h = s / c * 2
    return h


def pos_floor(pos):
    """
    对坐标进行向下取整。

    支持n维坐标。

    -----

    :param tuple[float] pos: 坐标

    :return: 取整后的坐标
    :rtype: tuple[int]
    """
    return tuple(int(floor(i)) for i in pos)


def pos_distance(pos1, pos2):
    """
    计算两个坐标间的距离。

    支持n维坐标。

    -----

    :param tuple[float] pos1: 坐标1
    :param tuple[float] pos2: 坐标2
        
    :return: 坐标距离，若任一坐标为None，返回-1.0
    :rtype: float
    """
    if not pos1 or not pos2:
        return -1.0
    return sqrt(sum((a - b)**2 for a, b in zip(pos1, pos2)))


def to_relative_pos(entity_pos1, entity_pos2):
    """
    将实体1的绝对坐标转换为相对实体2的坐标。
        
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
    将实体的世界坐标转换为屏幕上的平面坐标，并根据玩家水平视角做对应旋转。

    可用于在小地图上显示实体图标。
        
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
    org_pos = (half_screen_size * ratio[0], half_screen_size * ratio[1])
    rotated_pos = pos_rotate(player_rot, org_pos)
    screen_pos = (
        half_screen_size - rotated_pos[0] - half_ui_size,
        half_screen_size - rotated_pos[1] - half_ui_size,
    )
    return screen_pos


def pos_rotate(angle, pos):
    """
    计算给定坐标绕坐标原点旋转后的新坐标。
        
    -----
    
    :param float angle: 旋转角
    :param tuple[float,float] pos: 原始坐标（二维坐标）
        
    :return: 旋转后的坐标
    :rtype: tuple[float,float]|None
    """
    if not angle or not pos:
        return
    radian = (-angle / 180) * pi
    rotate_x = cos(radian) * pos[0] - sin(radian) * pos[1]
    rotate_y = cos(radian) * pos[1] + sin(radian) * pos[0]
    return rotate_x, rotate_y


def midpoint(first_point, second_point):
    """
    计算给定两点间的中点坐标。
        
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
    计算从 ``pos1`` 指向 ``pos2`` 的相机角度。

    可用于将玩家相机视角锁定到某一坐标。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: (竖直角度, 水平角度)
    :rtype: tuple[float,float]|None
    """
    if not pos1 or not pos2:
        return
    vec = Vector3(pos2) - Vector3(pos1)
    rot = get_api().GetRotFromDir(vec.ToTuple())
    return rot


def pos_entity_facing(entity_id, dist, use_0yaw=False, height_offset=0.0):
    """
    计算实体视角方向上、给定距离上的位置的坐标。

    -----

    :param str entity_id: 实体ID
    :param float dist: 距离
    :param bool use_0yaw: 是否使用0作为实体竖直方向上的视角
    :param float height_offset: 高度偏移量（如实体为玩家建议使用1.6，其他实体建议使用其头部到脚底的距离）

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    comp_factory = get_comp_factory()
    rot = comp_factory.CreateRot(entity_id).GetRot()
    if not rot:
        return
    if use_0yaw:
        rot = (0, rot[1])
    direction = get_api().GetDirFromRot(rot)
    ep = comp_factory.CreatePos(entity_id).GetFootPos()
    if not ep:
        return
    ep = (ep[0], ep[1] + height_offset, ep[2])
    return tuple(p + d * dist for p, d in zip(ep, direction))


def pos_forward_rot(pos, rot, dist):
    """
    计算从 ``pos`` 射出，以 ``rot`` 为方向的射线上，与 ``pos`` 的距离为 ``dist`` 的位置的坐标。

    -----

    :param tuple[float,float,float] pos: 坐标
    :param tuple[float,float] rot: (竖直角度, 水平角度)
    :param float dist: 距离

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not rot or not pos:
        return
    direction = get_api().GetDirFromRot(rot)
    return tuple(p + d * dist for p, d in zip(pos, direction))


def n_quantiles_index_list(n, data):
    """
    计算一串数据的n分位数的位置。

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
    计算立方体中心坐标。

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
    计算立方体最大棱长。
        
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


def is_in_cylinder(pos, r, center1, center2):
    """
    判断给定坐标是否在圆柱体区域内。

    -----

    :param tuple[float,float,float] pos: 坐标
    :param float r: 圆柱体半径
    :param tuple[float,float,float] center1: 圆柱体底面中心坐标
    :param tuple[float,float,float] center2: 圆柱体另一底面中心坐标

    :return: 在圆柱体区域内则返回True，否则返回False
    :rtype: bool
    """
    pos = Vector(pos)
    center1 = Vector(center1)
    center2 = Vector(center2)
    axis_vec = center2 - center1
    axis_len2 = axis_vec.length2
    pos_vec = pos - center1
    pos_len2 = pos_vec.length2
    r2 = r**2
    t = axis_vec.dot(pos_vec) / axis_len2
    if t < 0 or t > 1:
        return False
    dist2 = pos_len2 - t * t * axis_len2
    return dist2 <= r2

def is_in_sector(pos, r, angle, center, direction):
    """
    判断给定坐标是否在扇形区域内。

    -----

    :param tuple[float,float,float] pos: 待测试的坐标
    :param float r: 扇形半径
    :param float angle: 扇形张开的角度
    :param tuple[float,float,float] center: 扇形圆心坐标
    :param tuple[float,float,float] direction: 扇形方向向量

    :return: 在扇形区域内则返回True，否则返回False
    :rtype: bool
    """
    pos = Vector(pos)
    center = Vector(center)
    direction = Vector(direction).normalize()
    v = pos - center
    dist2 = v.length2
    if dist2 > r**2:
        return False
    v_len = sqrt(dist2)
    if v_len <= 0:
        return True
    cos_alpha = v.dot(direction) / v_len
    theta = radians(angle)
    cos_theta_half = cos(theta / 2.0)
    return cos_alpha >= cos_theta_half


def _num_in_range(num, r1, r2):
    return r1 <= num <= r2 or r2 <= num <= r1


def is_in_cube(obj, pos1, pos2, ignore_y=False):
    """
    判断对象是否在立方体区域内。
        
    -----
    
    :param str|tuple[float,float,float] obj: 实体ID或坐标
    :param tuple[float,float,float] pos1: 立方体对角顶点坐标1
    :param tuple[float,float,float] pos2: 立方体对角顶点坐标2
    :param bool ignore_y: 是否忽略Y轴
        
    :return: 在立方体区域内返回True，否则返回False
    :rtype: bool
    """
    if isinstance(obj, str):
        target_pos = get_comp_factory().CreatePos(obj).GetFootPos()
    else:
        target_pos = obj
    if not target_pos or not pos1 or not pos2:
        return False
    for i in range(3):
        if ignore_y and i == 1:
            continue
        if not _num_in_range(target_pos[i], pos1[i], pos2[i]):
            return False
    return True


def rot_diff(r1, r2):
    """
    计算两个角度之间的实际差值。
        
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
    从指定位置射出一条射线，计算该射线与指定立方体（AABB）的第一个交点坐标，不相交时返回 ``None`` 。

    -----

    :param tuple[float,float,float] ray_start_pos: 射线起始坐标
    :param tuple[float,float,float] ray_dir: 射线方向向量（单位向量）
    :param float length: 射线长度
    :param tuple[float,float,float] cube_center_pos: 立方体中心坐标
    :param tuple[float,float,float] cube_size: 立方体边长元组，分别对应xyz上的边长

    :return: 射线与立方体的第一个交点坐标，不相交时返回None
    :rtype: tuple[float,float,float]|None
    """
    ray_start_pos = Vector3(ray_start_pos)
    ray_dir = Vector3(ray_dir)
    cube_center_pos = Vector3(cube_center_pos)
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
    从指定位置射出一条射线，获取该射线经过的方块。

    返回一个列表，方块按照由近到远的顺序排列，列表每个元素为一个字典，结构如下：

    ::

        {
            'name': str,                                # 方块ID
            'aux': int,                                 # 方块特殊值
            'pos': Tuple[float, float, float],          # 方块坐标
            'intersection': Tuple[float, float, float], # 射线与方块的第一个交点的坐标
        }

    -----

    | 算法作者：头脑风暴
    | 修改：`Nuoyan <https://github.com/charminglee>`_

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
        start = int(floor(s))
        end = int(floor(s + d * length))
        step_range = range(start + 1, end + 1) if d > 0 else range(start, end, -1)
        for i in step_range:
            t_list.append((i - s) / d)
    t_list.sort()
    t_list = t_list[:-1]
    comp = get_comp_factory().CreateBlockInfo(LEVEL_ID)
    block_list = []
    for t in t_list:
        block_pos = [0, 0, 0]
        intersection = [0, 0, 0]
        for n in range(3):
            pos_val = start_pos[n] + t * direction[n]
            intersection[n] = pos_val
            if pos_val.is_integer() and direction[n] < 0:
                pos_val -= 1
            block_pos[n] = int(floor(pos_val))
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















