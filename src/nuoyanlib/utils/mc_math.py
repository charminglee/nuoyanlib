# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-19
#  ⠀
# =================================================


import math
import random
from mod.common.minecraftEnum import Facing
from ..core._sys import get_api, get_cf
from ..core._utils import inject_is_client, UNIVERSAL_OBJECT
from .vector import Vector


__all__ = [
    "distance2nearest_entity",
    "distance2nearest_player",
    "distance2line",
    "distance_square",
    "distance",
    "chunk_pos",
    "polar_coord",
    "cartesian_coord",
    "relative_pos",
    "absolute_pos",
    "screen_pos",
    "box_min_max",
    "pos_entity_facing",
    "pos_block_facing",
    "pos_forward_rot",
    "pos_floor",
    "pos_rotate",
    "midpoint",
    "box_center",
    "ray_box_intersection",
    "is_in_cylinder",
    "is_in_sector",
    "is_in_box",
    "range_map",
    "clamp",
    "probability",
    "box_max_edge_len",
    "camera_rot_p2p",
]


if 0:
    # 绕过机审专用
    distance2nearest_entity = lambda *_, **__: UNIVERSAL_OBJECT
    distance2nearest_player = lambda *_, **__: UNIVERSAL_OBJECT
    distance_square = lambda *_, **__: UNIVERSAL_OBJECT
    distance = lambda *_, **__: UNIVERSAL_OBJECT
    pos_entity_facing = lambda *_, **__: UNIVERSAL_OBJECT
    pos_forward_rot = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_cylinder = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_sector = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_box = lambda *_, **__: UNIVERSAL_OBJECT
    camera_rot_p2p = lambda *_, **__: UNIVERSAL_OBJECT


_INF = float('inf')
_NAN = float('nan')
_ZERO_EPS = 1e-8


def _to_pos(target, is_client=None):
    return get_cf(target, is_client).Pos.GetFootPos() if isinstance(target, str) else target


def _get_dim(entity_id):
    return get_cf(entity_id, False).Dimension.GetEntityDimensionId()


# region Distance ======================================================================================================


@inject_is_client
def distance2nearest_entity(__is_client__, target, dim=None):
    """
    计算坐标或实体与其距离最近的实体的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param int|None dim: 维度ID；若当前为客户端或 target 为实体ID，可忽略该参数；默认为 None

    :return: 与距离最近的实体的距离；若找不到最近实体，返回 float('inf')
    :rtype: float
    """
    api = get_api(__is_client__)
    if not __is_client__ and isinstance(target, str):
        dim = _get_dim(target)

    min_dist2 = _INF
    all_entities = api.GetEngineActor()
    for player_id in api.GetPlayerList():
        all_entities[player_id] = {'dimensionId': _get_dim(player_id)}

    for entity_id, data in all_entities:
        if not __is_client__ and data['dimensionId'] != dim:
            continue
        dist2 = distance_square(target, entity_id)
        if dist2 < min_dist2:
            min_dist2 = dist2
    return math.sqrt(min_dist2)


@inject_is_client
def distance2nearest_player(__is_client__, target, dim=None):
    """
    计算坐标或实体与其距离最近的玩家的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param int|None dim: 维度ID；若当前为客户端或 target 为实体ID，可忽略该参数；默认为 None

    :return: 与距离最近的玩家的距离；若找不到最近玩家，返回 float('inf')
    :rtype: float
    """
    api = get_api(__is_client__)
    if not __is_client__ and isinstance(target, str):
        dim = _get_dim(target)

    min_dist2 = _INF
    all_players = api.GetPlayerList()
    for player_id in all_players:
        if not __is_client__ and _get_dim(player_id) != dim:
            continue
        dist2 = distance_square(target, player_id)
        if dist2 < min_dist2:
            min_dist2 = dist2
    return math.sqrt(min_dist2)


def distance2line(target, line_pos1, line_pos2):
    """
    计算坐标或实体与某一直线的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param tuple[float,float,float] line_pos1: 直线上任意一点的坐标
    :param tuple[float,float,float] line_pos2: 直线上另一点的坐标，不能与line_pos1一致

    :return: 与指定直线的距离；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    a = distance(target, line_pos1)
    b = distance(target, line_pos2)
    c = distance(line_pos1, line_pos2)
    if a == _INF or b == _INF or c == _INF:
        return _INF
    p = (a + b + c) / 2
    s = math.sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / c * 2
    return h


@inject_is_client
def distance_square(__is_client__, target1, target2):
    """
    计算两个坐标或实体间距离的平方，相比于直接计算距离速度更快。

    -----

    :param tuple[float]|str target1: 坐标或实体ID
    :param tuple[float]|str target2: 坐标或实体ID

    :return: 距离的平方；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    p1, p2 = _to_pos(target1, __is_client__), _to_pos(target2, __is_client__)
    if not p1 or not p2:
        return _INF
    return sum((a - b)**2 for a, b in zip(p1, p2))


@inject_is_client
def distance(__is_client__, target1, target2):
    """
    计算两个坐标或实体间的距离。

    -----

    :param tuple[float]|str target1: 坐标或实体ID
    :param tuple[float]|str target2: 坐标或实体ID

    :return: 距离；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    p1, p2 = _to_pos(target1, __is_client__), _to_pos(target2, __is_client__)
    if not p1 or not p2:
        return _INF
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


# endregion


# region Coordinate Transformation =====================================================================================


def chunk_pos(pos):
    """
    将世界坐标转换为区块坐标。

    -----

    :param tuple[float,float,float] pos: 世界坐标

    :return: 区块坐标
    :rtype: tuple[int,int]|None
    """
    if not pos:
        return
    pos = pos_floor(pos)
    return int(pos[0] // 16), int(pos[2] // 16)


def polar_coord(coord, rad=False, origin=(0, 0)):
    """
    将平面直角坐标转换为极坐标。

    -----

    :param tuple[float,float] coord: 平面直角坐标
    :param bool rad: 是否使用弧度制，默认为False
    :param tuple[float,float] origin: 坐标原点，默认为(0, 0)

    :return: 极坐标
    :rtype: tuple[float,float]
    """
    x, y = coord
    x -= origin[0]
    y -= origin[1]
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    if not rad:
        theta = math.degrees(theta)
    return r, theta


def cartesian_coord(coord, rad=False, origin=(0, 0)):
    """
    将极坐标转换为平面直角坐标。

    -----

    :param tuple[float,float] coord: 极坐标
    :param bool rad: 是否使用弧度制，默认为False
    :param tuple[float,float] origin: 坐标原点，默认为(0, 0)

    :return: 平面直角坐标
    :rtype: tuple[float,float]
    """
    r, theta = coord
    if not rad:
        theta = math.radians(theta)
    x = r * math.cos(theta) + origin[0]
    y = r * math.sin(theta) + origin[1]
    return x, y


def relative_pos(pos, basis):
    """
    根据基准坐标将绝对坐标转换为相对坐标。

    -----

    :param tuple[float] pos: 绝对坐标
    :param tuple[float] basis: 基准坐标

    :return: 相对坐标
    :rtype: tuple[float]|None
    """
    if not basis or not pos:
        return
    return tuple(p - b for p, b in zip(pos, basis))


def absolute_pos(pos, basis):
    """
    根据基准坐标将相对坐标转换为绝对坐标。

    -----

    :param tuple[float] pos: 相对坐标
    :param tuple[float] basis: 基准坐标

    :return: 绝对坐标
    :rtype: tuple[float]|None
    """
    if not basis or not pos:
        return
    return tuple(p + b for p, b in zip(pos, basis))


def screen_pos(pos, world_basis, screen_basis=(0, 0), scale=1, offset=(0, 0), rotation=0, rad=False):
    """
    将世界坐标转换为屏幕坐标。

    在屏幕坐标系中，向右为X轴正方向，向下为Y轴正方向。在默认情况下，屏幕坐标系原点位于屏幕左上角。

    -----

    :param tuple[float,float,float] pos: 世界坐标
    :param tuple[float,float,float] world_basis: 屏幕坐标系原点对应的世界坐标
    :param tuple[float,float] screen_basis: 屏幕坐标系原点，默认为 (0, 0)
    :param float scale: 屏幕上1像素所对应的世界距离；默认为1
    :param tuple[float,float] offset: 屏幕坐标xy偏移量，默认为 (0, 0)
    :param float rotation: 绕坐标原点的旋转角度，默认为0
    :param bool rad: 旋转角是否使用弧度制，默认为False

    :return: 屏幕坐标
    :rtype: tuple[float,float]|None
    """
    if not pos or not world_basis:
        return
    scale = float(scale)
    rel_pos = relative_pos(pos, world_basis)
    scr_rel_pos = (
        rel_pos[0] / scale,
        rel_pos[2] / scale,
    )
    scr_rel_pos = pos_rotate(scr_rel_pos, rotation, rad=rad)
    scr_pos = (
        screen_basis[0] - scr_rel_pos[0] + offset[0],
        screen_basis[1] - scr_rel_pos[1] + offset[1],
    )
    return scr_pos


# endregion


# region Coordinate Calculation ========================================================================================


def box_min_max(pos1, pos2):
    """
    根据任意两个对角坐标，计算以这两点为顶点的包围盒的最小点和最大点坐标。

    -----

    :param tuple[float] pos1: 对角坐标1
    :param tuple[float] pos2: 对角坐标2

    :return: 最小点和最大点坐标
    :rtype: tuple[tuple[float],tuple[float]]|None
    """
    if not pos1 or not pos2:
        return
    if len(pos1) == 3:
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        return (x1, y1, z1), (x2, y2, z2)
    else:
        x1, y1 = pos1
        x2, y2 = pos2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        return (x1, y1), (x2, y2)


@inject_is_client
def pos_entity_facing(__is_client__, entity_id, dist, use_0yaw=False, height_offset=0):
    """
    计算实体视角方向上、给定距离上的位置的坐标。

    计算将以实体 FootPos 作为起点，沿实体视角方向前进指定距离后的位置即为最终结果。
    可通过 ``height_offset`` 参数调整起点的高度偏移量，最终的起点坐标为：
    ::

        (FootPos[0], FootPos[1] + height_offset, FootPos[2])
    若实体为玩家，将 ``height_offset`` 设为 ``1.63`` 即可使起点位于眼睛（准星）位置。

    -----

    :param str entity_id: 实体ID
    :param float dist: 距离，可为负数
    :param bool use_0yaw: 是否将实体竖直方向上的视角视为0，默认为False
    :param float height_offset: 高度偏移量，默认为0

    :return: 坐标；若实体不存在，返回 None
    :rtype: tuple[float,float,float]|None
    """
    cf = get_cf(entity_id, __is_client__)
    api = get_api(__is_client__)
    rot = cf.Rot.GetRot()
    if not rot:
        return
    if use_0yaw:
        rot = (0, rot[1])
    direction = api.GetDirFromRot(rot)
    pos = cf.Pos.GetFootPos()
    if not pos:
        return
    pos = (pos[0], pos[1] + height_offset, pos[2])
    return tuple(p + d * dist for p, d in zip(pos, direction))


def pos_block_facing(pos, face=Facing.North, dist=1.0):
    """
    计算某一方块朝向上（东西南北上下）、给定距离上的位置的坐标。

    -----

    :param tuple[float,float,float] pos: 起始坐标
    :param int face: 方块朝向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_，默认为 Facing.North
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
    raise ValueError("invalid face value")


@inject_is_client
def pos_forward_rot(__is_client__, pos, rot, dist):
    """
    计算以指定坐标为起点，沿指定视角方向前进指定距离后的坐标。

    -----

    :param tuple[float,float,float] pos: 起点坐标
    :param tuple[float,float] rot: 视角：(竖直角度, 水平角度)
    :param float dist: 距离

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not pos or not rot:
        return
    direction = get_api(__is_client__).GetDirFromRot(rot)
    return tuple(p + d * dist for p, d in zip(pos, direction))


def pos_floor(pos):
    """
    对坐标进行向下取整。

    -----

    :param tuple[float] pos: 坐标

    :return: 取整后的坐标
    :rtype: tuple[int]|None
    """
    if not pos:
        return
    return tuple(int(i // 1) for i in pos)


def pos_rotate(pos, angle, basis=(0, 0), rad=False):
    """
    计算二维坐标绕指定坐标旋转后的新坐标。

    -----

    :param tuple[float,float] pos: 二维坐标
    :param float angle: 旋转角
    :param tuple[float,float] basis: 旋转中心坐标，默认为 (0, 0)
    :param bool rad: 旋转角是否使用弧度制，默认为False

    :return: 旋转后的坐标
    :rtype: tuple[float,float]|None
    """
    if not rad:
        angle = math.radians(angle)
    x, y = pos
    bx, by = basis
    x -= bx
    y -= by
    return (
        bx + x * math.cos(angle) - y * math.sin(angle),
        by + y * math.cos(angle) + x * math.sin(angle),
    )


def midpoint(pos1, pos2):
    """
    计算给定两点的中点坐标。

    -----

    :param tuple[float] pos1: 坐标1
    :param tuple[float] pos2: 坐标2

    :return: 中点坐标
    :rtype: tuple[float]|None
    """
    if not pos1 or not pos2:
        return
    return tuple((a + b) / 2.0 for a, b in zip(pos1, pos2))


def box_center(pos1, pos2):
    """
    计算包围盒中心坐标。

    -----

    :param tuple[float] pos1: 包围盒对角顶点坐标1
    :param tuple[float] pos2: 包围盒对角顶点坐标2

    :return: 中心坐标
    :rtype: tuple[float]|None
    """
    return midpoint(pos1, pos2)


def ray_box_intersection(start_pos, ray_dir, length, aabb_center, aabb_size, handle_inside="none"):
    """
    计算射线与指定包围盒的第一个交点的坐标，未相交时返回 ``None`` 。

    -----

    :param tuple[float,float,float] start_pos: 射线起点坐标
    :param tuple[float,float,float] ray_dir: 射线方向向量
    :param float length: 射线长度，传入-1表示无限长
    :param tuple[float,float,float] aabb_center: 包围盒中心坐标
    :param tuple[float,float,float] aabb_size: 包围盒边长元组，分别对应xyz上的边长
    :param str handle_inside: 当射线起点在包围盒内部时的处理方式，可选值为 "none"（返回 None），"start"（返回射线起点坐标） 或 "exit"（返回射线穿出包围盒时的位置）；默认为 "none"

    :return: 射线与包围盒的第一个交点的坐标，未相交时返回 None
    :rtype: tuple[float,float,float]|None
    """
    start_pos_tuple = start_pos
    start_pos = Vector(start_pos)
    ray_dir = Vector(ray_dir)
    ray_dir.normalize()
    if length < 0:
        length = _INF
    local_start_pos = start_pos - aabb_center
    t_min = -float('inf')
    t_max = float('inf')

    for i in range(3):
        half_size = aabb_size[i] / 2.0
        start = local_start_pos[i]
        d = ray_dir[i]
        if abs(d) < _ZERO_EPS:
            # 射线与某一坐标轴垂直时，检查起点是否在包围盒该轴范围内
            if start < -half_size or start > half_size:
                return
        else:
            t1 = (-half_size - start) / d
            t2 = (half_size - start) / d
            if t1 > t2:
                t1, t2 = t2, t1
            if t1 > t_min:
                t_min = t1
            if t2 < t_max:
                t_max = t2

    # 若进入点大于离开点或包围盒在射线后方，则未相交
    if t_min > t_max or t_max < 0:
        return

    # 处理起点在包围盒内部的情况
    if t_min < 0:
        if handle_inside == "start":
            return start_pos_tuple
        elif handle_inside == "exit":
            return tuple(start_pos + ray_dir * t_max) if t_max <= length else None
        return

    # 一般情况，返回进入点
    if t_min <= length:
        return tuple(start_pos + ray_dir * t_min)


# endregion


# region Area Test =====================================================================================================


@inject_is_client
def is_in_cylinder(__is_client__, target, r, center1, center2):
    """
    判断坐标或实体是否在圆柱体区域内。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param float r: 圆柱体半径
    :param tuple[float,float,float] center1: 圆柱体底面中心坐标
    :param tuple[float,float,float] center2: 圆柱体另一底面中心坐标

    :return: 是否在圆柱体区域内
    :rtype: bool
    """
    tp = _to_pos(target, __is_client__)
    if not tp:
        return False
    tp = Vector(tp)
    center1 = Vector(center1)
    center2 = Vector(center2)
    axis_vec = center2 - center1
    axis_len2 = axis_vec.length2
    pos_vec = tp - center1
    pos_len2 = pos_vec.length2
    r2 = r**2
    t = axis_vec.dot(pos_vec) / axis_len2
    if t < 0 or t > 1:
        return False
    dist2 = pos_len2 - t * t * axis_len2
    return dist2 <= r2


@inject_is_client
def is_in_sector(__is_client__, target, r, h, angle, center, direction):
    """
    判断坐标或实体是否在扇形（饼状三维扇形）区域内。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param float r: 扇形半径
    :param float h: 扇形高度
    :param float angle: 扇形张开的角度（角度制）
    :param tuple[float,float,float] center: 扇形圆心坐标
    :param tuple[float,float,float] direction: 扇形方向向量

    :return: 是否在扇形区域内
    :rtype: bool
    """
    tp = _to_pos(target, __is_client__)
    if not tp:
        return False

    v = Vector(tp) - center
    dist2 = v.length2
    # 目标位于圆心
    if dist2 <= _ZERO_EPS:
        return True

    d = Vector(direction).normalize()
    proj = v.dot(d)
    # 目标在扇形背后或超出半径
    if proj < 0 or proj > r:
        return False
    # 超出扇形高度范围
    if dist2 - proj**2 > h**2 / 4.0:
        return False

    v_len = math.sqrt(dist2)
    cos_alpha = proj / v_len
    theta = math.radians(angle / 2.0)
    cos_theta = math.cos(theta)
    return cos_alpha >= cos_theta


@inject_is_client
def is_in_box(__is_client__, target, pos1, pos2, ignore_y=False):
    """
    判断坐标或实体是否在包围盒内。

    -----

    :param tuple[float]|str target: 坐标或实体ID
    :param tuple[float] pos1: 包围盒对角顶点坐标1
    :param tuple[float] pos2: 包围盒对角顶点坐标2
    :param bool ignore_y: 是否忽略Y轴，默认为False

    :return: 是否在包围盒内
    :rtype: bool
    """
    tp = _to_pos(target, __is_client__)
    if not tp:
        return False
    pos1, pos2 = box_min_max(pos1, pos2)
    if tp[0] < pos1[0] or tp[0] > pos2[0]:
        return False
    if not ignore_y and (tp[1] < pos1[1] or tp[1] > pos2[1]):
        return False
    if len(tp) == 3 and (tp[2] < pos1[2] or tp[2] > pos2[2]):
        return False
    return True


# endregion


# region Misc ==========================================================================================================


def range_map(x, output_range, input_range=[0, 1], func=None): # noqa
    """
    将某个区间内的数值映射到另一个区间。

    -----

    :param float x: 输入值
    :param tuple[float,float] output_range: 输出区间（闭区间）
    :param tuple[float,float] input_range: 输入区间（闭区间），默认为 [0, 1]
    :param function func: 插值函数，接受一个参数 t ∈ [0, 1]，返回 [0, 1] 的值；默认为 None

    :return: 映射值
    :rtype: float
    """
    j, k = output_range
    m, n = input_range
    t = float(x - m) / (n - m)
    if func:
        t = func(t)
    return j + (k - j) * t


def clamp(x, min_value, max_value):
    """
    将数值限制在指定范围内。

    小于 ``min_value`` 的值将被限制为 ``min_value`` ，大于 ``max_value`` 的值将被限制为 ``max_value`` 。

    -----

    :param float x: 数值
    :param float min_value: 最小值
    :param float max_value: 最大值

    :return: 限制值
    :rtype: float
    """
    return max(min_value, min(max_value, x))


def probability(p):
    """
    以指定概率返回 ``True`` 。

    -----

    :param float p: 概率，范围为 [0, 1]

    :return: 以 p 的概率返回 True，否则返回 False
    :rtype: bool
    """
    return p > random.random()


def box_max_edge_len(pos1, pos2):
    """
    计算包围盒最大棱长。
        
    -----
    
    :param tuple[float] pos1: 包围盒对角坐标1
    :param tuple[float] pos2: 包围盒对角坐标2
        
    :return: 包围盒最大棱长
    :rtype: float
    """
    return max(abs(a - b) for a, b in zip(pos1, pos2))


@inject_is_client
def camera_rot_p2p(__is_client__, pos1, pos2):
    """
    计算从 ``pos1`` 指向 ``pos2`` 的相机角度。

    可用于将实体相机视角锁定到某一坐标。

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: 相机角度：(竖直角度, 水平角度)
    :rtype: tuple[float,float]|None
    """
    if not pos1 or not pos2:
        return
    api = get_api(__is_client__)
    return api.GetRotFromDir(
        pos2[0] - pos1[0],
        pos2[1] - pos1[1],
        pos2[2] - pos1[2],
    )


# endregion















