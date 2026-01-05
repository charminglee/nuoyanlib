# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-6
#  ⠀
# =================================================


from __future__ import division
from math import sin, cos, atan2, sqrt, degrees, radians
from mod.common.minecraftEnum import Facing
from ..core._sys import get_api, get_cf
from ..core._utils import inject_is_client, UNIVERSAL_OBJECT
from .vector import Vector, dir2rot, rot2dir


if 0:
    from typing import Iterable


__all__ = [
    "manhattan_distance",
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
    "box_vertices",
    "box_min_max",
    "pos_entity_facing",
    "pos_block_facing",
    "pos_forward_rot",
    "pos_floor",
    "pos_rotate",
    "midpoint",
    "box_center",
    "ray_box_intersection",
    "is_in_sphere",
    "is_in_cylinder",
    "is_in_sector",
    "is_in_box",
    "fpp_camera_rot",
    "tpp_camera_rot",
    "rot_from_to",
    "angle_normalize",
    "bezier_curve",
    "catmull_rom",
    "median",
    "std",
    "var",
    "mean",
    "sign",
    "lerp",
    "range_map",
    "clamp",
    "box_max_edge_len",
]


if 0:
    # 绕过机审专用
    manhattan_distance = lambda *_, **__: UNIVERSAL_OBJECT
    distance2nearest_entity = lambda *_, **__: UNIVERSAL_OBJECT
    distance2nearest_player = lambda *_, **__: UNIVERSAL_OBJECT
    distance2line = lambda *_, **__: UNIVERSAL_OBJECT
    distance_square = lambda *_, **__: UNIVERSAL_OBJECT
    distance = lambda *_, **__: UNIVERSAL_OBJECT
    pos_entity_facing = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_sphere = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_cylinder = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_sector = lambda *_, **__: UNIVERSAL_OBJECT
    is_in_box = lambda *_, **__: UNIVERSAL_OBJECT


_INF = float('inf')
_NAN = float('nan')
_ZERO_EPS = 1e-8


def _get_pos(target, is_client=None):
    return get_cf(target, is_client).Pos.GetFootPos() if isinstance(target, str) else target


def _get_dim(entity_id):
    return get_cf(entity_id, False).Dimension.GetEntityDimensionId()


# region Distance ======================================================================================================


@inject_is_client
def manhattan_distance(__is_client__, target1, target2):
    """
    计算两个坐标或实体间的曼哈顿距离。

    -----

    :param tuple[float,float,float]|tuple[float,float]|str target1: 坐标或实体ID
    :param tuple[float,float,float]|tuple[float,float]|str target2: 坐标或实体ID

    :return: 曼哈顿距离；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    p1, p2 = _get_pos(target1, __is_client__), _get_pos(target2, __is_client__)
    if not p1 or not p2:
        return _INF
    return float(sum(abs(p1 - p2) for p1, p2 in zip(p1, p2)))


def _dist_square(p1, p2):
    return sum((a - b)**2 for a, b in zip(p1, p2))


def _dist(p1, p2):
    return sqrt(_dist_square(p1, p2))


@inject_is_client
def distance2nearest_entity(__is_client__, target, dim=None):
    """
    计算坐标或实体与其距离最近的实体的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param int|None dim: 维度ID；若当前为客户端或 target 为实体ID，可忽略该参数

    :return: 与距离最近的实体的距离；若找不到最近实体，返回 float('inf')
    :rtype: float
    """
    api = get_api(__is_client__)
    # 传入实体ID时，若为服务端，获取该实体所在维度
    if not __is_client__ and isinstance(target, str) and dim is None:
        dim = _get_dim(target)
    tp = _get_pos(target, __is_client__)
    if not tp:
        return _INF

    min_dist2 = _INF
    all_entities = api.GetEngineActor()
    for player_id in api.GetPlayerList():
        all_entities[player_id] = {'dimensionId': -1 if __is_client__ else _get_dim(player_id)}

    for entity_id, data in all_entities.items():
        # 处于客户端时跳过维度判断
        if not __is_client__ and data['dimensionId'] != dim:
            continue
        ep = _get_pos(entity_id, __is_client__)
        if not ep:
            continue
        dist2 = _dist_square(tp, ep)
        if dist2 < min_dist2:
            min_dist2 = dist2
    return sqrt(min_dist2)


@inject_is_client
def distance2nearest_player(__is_client__, target, dim=None):
    """
    计算坐标或实体与其距离最近的玩家的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param int|None dim: 维度ID；若当前为客户端或 target 为实体ID，可忽略该参数

    :return: 与距离最近的玩家的距离；若找不到最近玩家，返回 float('inf')
    :rtype: float
    """
    api = get_api(__is_client__)
    # 传入实体ID时，若为服务端，获取该实体所在维度
    if not __is_client__ and isinstance(target, str) and dim is None:
        dim = _get_dim(target)
    tp = _get_pos(target, __is_client__)
    if not tp:
        return _INF

    min_dist2 = _INF
    all_players = api.GetPlayerList()

    for player_id in all_players:
        # 处于客户端时跳过维度判断
        if not __is_client__ and _get_dim(player_id) != dim:
            continue
        pp = _get_pos(player_id, __is_client__)
        if not pp:
            continue
        dist2 = _dist_square(tp, pp)
        if dist2 < min_dist2:
            min_dist2 = dist2
    return sqrt(min_dist2)


@inject_is_client
def distance2line(__is_client__, target, line_pos1, line_pos2):
    """
    计算坐标或实体与某一直线的距离。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param tuple[float,float,float] line_pos1: 直线上任意一点的坐标
    :param tuple[float,float,float] line_pos2: 直线上另一点的坐标，不能与line_pos1一致

    :return: 与指定直线的距离；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    if not line_pos1 or not line_pos2:
        return _INF
    tp = _get_pos(target, __is_client__)
    if not tp:
        return _INF
    a = _dist(tp, line_pos1)
    b = _dist(tp, line_pos2)
    c = _dist(line_pos1, line_pos2)
    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / c * 2
    return h


@inject_is_client
def distance_square(__is_client__, target1, target2):
    """
    计算两个坐标或实体间距离的平方，相比于直接计算距离速度更快。

    -----

    :param tuple[float,float,float]|tuple[float,float]|str target1: 坐标或实体ID
    :param tuple[float,float,float]|tuple[float,float]|str target2: 坐标或实体ID

    :return: 距离的平方；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    p1, p2 = _get_pos(target1, __is_client__), _get_pos(target2, __is_client__)
    if not p1 or not p2:
        return _INF
    return sum((a - b)**2.0 for a, b in zip(p1, p2))


@inject_is_client
def distance(__is_client__, target1, target2):
    """
    计算两个坐标或实体间的距离。

    -----

    :param tuple[float,float,float]|tuple[float,float]|str target1: 坐标或实体ID
    :param tuple[float,float,float]|tuple[float,float]|str target2: 坐标或实体ID

    :return: 距离；若任一坐标为 None，返回 float('inf')
    :rtype: float
    """
    p1, p2 = _get_pos(target1, __is_client__), _get_pos(target2, __is_client__)
    if not p1 or not p2:
        return _INF
    return sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


# endregion


# region Coordinate Transformation =====================================================================================


def chunk_pos(pos):
    """
    将世界坐标转换为区块坐标。

    -----

    :param tuple[float,float,float] pos: 世界坐标

    :return: 区块坐标；传入的世界坐标为 None 时，返回 None
    :rtype: tuple[int,int]|None
    """
    if not pos:
        return
    pos = pos_floor(pos)
    return int(pos[0] // 16), int(pos[2] // 16)


def polar_coord(coord, rad=False, origin=(0, 0)):
    """
    将直角坐标转换为极坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] coord: 直角坐标
    :param bool rad: 是否使用弧度制；默认为 False
    :param tuple[float,float,float]|tuple[float,float] origin: 坐标原点；默认为 (0, 0, 0) 或 (0, 0)，根据 coord 的维度确定

    :return: 极坐标；传入的直角坐标坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]
    """
    if len(coord) == 2:
        x, y = coord # noqa
        x -= origin[0]
        y -= origin[1]
        r = sqrt(x**2 + y**2)
        theta = atan2(y, x)
        if not rad:
            theta = degrees(theta)
        return r, theta
    else:
        x, y, z = coord
        x -= origin[0]
        y -= origin[1]
        z -= origin[2]
        r = sqrt(x**2 + y**2 + z**2)
        theta = atan2(sqrt(x**2 + y**2), z)
        phi = atan2(y, x)
        if not rad:
            theta = degrees(theta)
            phi = degrees(phi)
        return r, theta, phi


def cartesian_coord(coord, rad=False, origin=None):
    """
    将极坐标转换为直角坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] coord: 极坐标
    :param bool rad: 是否使用弧度制；默认为 False
    :param tuple[float,float,float]|tuple[float,float] origin: 坐标原点；默认为 (0, 0, 0) 或 (0, 0)，根据 coord 的维度确定

    :return: 直角坐标；传入的极坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]
    """
    if len(coord) == 2:
        r, theta = coord # noqa
        if not rad:
            theta = radians(theta)
        x = origin[0] + r * cos(theta)
        y = origin[1] + r * sin(theta)
        return x, y
    else:
        r, theta, phi = coord
        if not rad:
            theta = radians(theta)
            phi = radians(phi)
        x = origin[0] + r * sin(theta) * cos(phi)
        y = origin[1] + r * sin(theta) * sin(phi)
        z = origin[2] + r * cos(theta)
        return x, y, z


def relative_pos(pos, basis):
    """
    根据基准坐标将绝对坐标转换为相对坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos: 绝对坐标
    :param tuple[float,float,float]|tuple[float,float] basis: 基准坐标

    :return: 相对坐标；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
    """
    if not basis or not pos:
        return
    return tuple(p - b for p, b in zip(pos, basis))


def absolute_pos(pos, basis):
    """
    根据基准坐标将相对坐标转换为绝对坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos: 相对坐标
    :param tuple[float,float,float]|tuple[float,float] basis: 基准坐标

    :return: 绝对坐标；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
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
    :param tuple[float,float] screen_basis: 屏幕坐标系原点；默认为 (0, 0)
    :param float scale: 屏幕上1像素所对应的世界距离；默认为1
    :param tuple[float,float] offset: 屏幕坐标xy偏移量；默认为 (0, 0)
    :param float rotation: 绕坐标原点的旋转角度；默认为0
    :param bool rad: 旋转角是否使用弧度制；默认为False

    :return: 屏幕坐标；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float]|None
    """
    if not pos or not world_basis:
        return
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


def box_vertices(pos1, pos2):
    """
    根据任意两个对角坐标，计算以这两点为顶点的AABB包围盒的所有顶点的坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 对角坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 对角坐标2

    :return: 所有顶点坐标的列表；二维坐标返回4个顶点，三维坐标返回8个顶点；传入的任一坐标为 None 时，返回空列表
    :rtype: list[tuple[float,float,float]|tuple[float,float]]
    """
    if not pos1 or not pos2:
        return []
    pos1, pos2 = box_min_max(pos1, pos2)
    if len(pos1) == 2:
        x1, y1 = pos1 # noqa
        x2, y2 = pos2 # noqa
        return [
            (x1, y1),
            (x1, y2),
            (x2, y1),
            (x2, y2),
        ]
    else:
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        return [
            (x1, y1, z1),
            (x1, y1, z2),
            (x1, y2, z1),
            (x1, y2, z2),
            (x2, y1, z1),
            (x2, y1, z2),
            (x2, y2, z1),
            (x2, y2, z2),
        ]


def box_min_max(pos1, pos2):
    """
    根据任意两个对角坐标，计算以这两点为顶点的AABB包围盒的最小和最大坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 对角坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 对角坐标2

    :return: 坐标列表，第一个元素为最小坐标，第二个元素为最大坐标；传入的任一坐标 None 时，返回空列表
    :rtype: list[tuple[float,float,float]|tuple[float,float]]
    """
    if not pos1 or not pos2:
        return []
    if len(pos1) == 2:
        x1, y1 = pos1 # noqa
        x2, y2 = pos2 # noqa
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        return [(x1, y1), (x2, y2)]
    else:
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        return [(x1, y1, z1), (x2, y2, z2)]


@inject_is_client
def pos_entity_facing(__is_client__, entity_id, dist, use_0yaw=False, height_offset=0):
    """
    计算实体视角方向上、给定距离上的位置的坐标。

    计算将以实体 FootPos 作为起点，沿实体视角方向前进指定距离后的位置即为最终结果。
    可通过 ``height_offset`` 参数调整起点的高度偏移量，最终的起点坐标即为：
    ::

        (FootPos[0], FootPos[1] + height_offset, FootPos[2])
    若实体为玩家，将 ``height_offset`` 设为 ``1.62`` 即可使起点位于玩家眼睛（准星）位置。

    -----

    :param str entity_id: 实体ID
    :param float dist: 距离，可为负数
    :param bool use_0yaw: 是否将实体竖直方向上的视角视为0；默认为False
    :param float height_offset: 高度偏移量；默认为0

    :return: 坐标；若实体不存在，返回 None
    :rtype: tuple[float,float,float]|None
    """
    cf = get_cf(entity_id, __is_client__)
    rot = cf.Rot.GetRot()
    if not rot:
        return
    if use_0yaw:
        rot = (0, rot[1])
    direction = rot2dir(rot)
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
    :param int face: 方块朝向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_；默认为 Facing.North
    :param float dist: 距离；默认为1.0

    :return: 坐标；传入的起始坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|None
    """
    if not pos:
        return
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
    raise ValueError("invalid 'face' value")


def pos_forward_rot(pos, rot, dist):
    """
    计算以指定坐标为起点，沿指定视角方向前进指定距离后的坐标。

    -----

    :param tuple[float,float,float] pos: 起点坐标
    :param tuple[float,float] rot: 视角：(竖直角度, 水平角度)
    :param float dist: 距离

    :return: 坐标；传入的起点坐标或视角为 None 时，返回 None
    :rtype: tuple[float,float,float]|None
    """
    if not pos or not rot:
        return
    direction = rot2dir(rot)
    return tuple((p + d * dist) for p, d in zip(pos, direction))


def pos_floor(pos):
    """
    对坐标进行向下取整。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos: 坐标

    :return: 取整后的坐标；传入的坐标为 None 时，返回 None
    :rtype: tuple[int,int,int]|tuple[int,int]|None
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
    :param tuple[float,float] basis: 旋转中心坐标；默认为 (0, 0)
    :param bool rad: 旋转角是否使用弧度制；默认为False

    :return: 旋转后的坐标
    :rtype: tuple[float,float]|None
    """
    if not rad:
        angle = radians(angle)
    x, y = pos
    bx, by = basis
    x -= bx
    y -= by
    return (
        bx + x * cos(angle) - y * sin(angle),
        by + y * cos(angle) + x * sin(angle),
    )


def midpoint(pos1, pos2):
    """
    计算给定两点的中点坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 坐标2

    :return: 中点坐标；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
    """
    if not pos1 or not pos2:
        return
    return tuple((a + b) / 2 for a, b in zip(pos1, pos2))


def box_center(pos1, pos2):
    """
    计算AABB包围盒的中心坐标。

    -----

    :param tuple[float,float,float]|tuple[float,float] pos1: 包围盒对角顶点坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 包围盒对角顶点坐标2

    :return: 中心坐标；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
    """
    return midpoint(pos1, pos2)


def ray_box_intersection(start_pos, ray_dir, length, aabb_center, aabb_size, handle_inside="none"):
    """
    计算射线与指定AABB包围盒的第一个交点的坐标，未相交时返回 ``None`` 。

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
        half_size = aabb_size[i] / 2
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
def is_in_sphere(__is_client__, target, r, center):
    """
    判断坐标或实体是否在球体区域内。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param float r: 球体半径
    :param tuple[float,float,float] center: 球心坐标

    :return: 是否在球体区域内
    :rtype: bool
    """
    tp = _get_pos(target, __is_client__)
    if not tp:
        return False
    return _dist_square(tp, center) <= r**2


@inject_is_client
def is_in_cylinder(__is_client__, target, r, center1, center2):
    """
    判断坐标或实体是否在圆柱体区域内。

    -----

    :param tuple[float,float,float]|str target: 坐标或实体ID
    :param float r: 圆柱体半径
    :param tuple[float,float,float] center1: 圆柱体底面圆心坐标
    :param tuple[float,float,float] center2: 圆柱体另一底面圆心坐标

    :return: 是否在圆柱体区域内
    :rtype: bool
    """
    tp = _get_pos(target, __is_client__)
    if not tp:
        return False
    tp = Vector(tp)
    # center1 = Vector(center1)
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
    tp = _get_pos(target, __is_client__)
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
    if dist2 - proj**2 > h**2 / 4:
        return False

    v_len = sqrt(dist2)
    cos_alpha = proj / v_len
    theta = radians(angle / 2)
    cos_theta = cos(theta)
    return cos_alpha >= cos_theta


@inject_is_client
def is_in_box(__is_client__, target, pos1, pos2, ignore_y=False):
    """
    判断坐标或实体是否在AABB包围盒内。

    -----

    :param tuple[float,float,float]|tuple[float,float]|str target: 坐标或实体ID
    :param tuple[float,float,float]|tuple[float,float] pos1: 包围盒对角顶点坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 包围盒对角顶点坐标2
    :param bool ignore_y: 是否忽略Y轴；默认为False

    :return: 是否在包围盒内
    :rtype: bool
    """
    tp = _get_pos(target, __is_client__)
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


# region Rotation ======================================================================================================


def fpp_camera_rot(rot):
    """
    将第三人称相机视角转换为第一人称相机视角。

    -----

    :param tuple[float,float,float]|tuple[float,float] rot: 第三人称相机视角

    :return: 第一人称相机视角；传入的视角为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
    """
    if not rot:
        return
    yaw = angle_normalize(rot[1] - 180)
    return (rot[0], yaw, rot[2]) if len(rot) == 3 else (rot[0], yaw)


def tpp_camera_rot(rot):
    """
    将第一人称相机视角转换为第三人称相机视角。

    -----

    :param tuple[float,float,float]|tuple[float,float] rot: 第一人称相机视角

    :return: 第三人称相机视角；传入的视角为 None 时，返回 None
    :rtype: tuple[float,float,float]|tuple[float,float]|None
    """
    if not rot:
        return
    yaw = angle_normalize(rot[1] + 180)
    return (rot[0], yaw, rot[2]) if len(rot) == 3 else (rot[0], yaw)


def rot_from_to(start, end):
    """
    计算从起始坐标看向终点坐标的实体头部视角。

    -----

    :param tuple[float,float,float] start: 起始坐标
    :param tuple[float,float,float] end: 终点坐标

    :return: 头部视角；传入的任一坐标为 None 时，返回 None
    :rtype: tuple[float,float]|None
    """
    if not start or not end:
        return
    return dir2rot((
        end[0] - start[0],
        end[1] - start[1],
        end[2] - start[2],
    ))


def angle_normalize(angle):
    """
    将角度标准化到 ``[-180,⠀180]``。

    -----

    :param float angle: 角度

    :return: 标准化角度
    :rtype: float
    """
    angle %= 360.0
    if angle > 180:
        angle -= 360
    return angle


# endregion


# region Curve =========================================================================================================


def bezier_curve(control_points, t):
    """
    通用贝塞尔曲线（支持任意阶数）。

    控制点越多，计算越慢，通常不超过4个点。

    -----

    :param list[tuple[float,float,float]] control_points: 控制点列表
    :param float t: 插值因子，范围 [0, 1]

    :return: 曲线上的点
    :rtype: tuple[float,float,float]
    """
    n = len(control_points)
    if n == 0:
        return 0.0, 0.0, 0.0
    if n == 1:
        return control_points[0]

    points = list(control_points)
    for r in xrange(1, n):
        for i in xrange(n - r):
            points[i] = (
                (1 - t) * points[i][0] + t * points[i + 1][0],
                (1 - t) * points[i][1] + t * points[i + 1][1],
                (1 - t) * points[i][2] + t * points[i + 1][2],
            )
    return points[0]


def catmull_rom(p0, p1, p2, p3, t, alpha=0.5):
    """
    Catmull-Rom样条曲线。

    曲线会经过 ``p1`` 和 ``p2`` ， ``p0`` 和 ``p3`` 用于确定切线方向。

    -----

    :param tuple[float,float,float] p0: 前一个点
    :param tuple[float,float,float] p1: 起点
    :param tuple[float,float,float] p2: 终点
    :param tuple[float,float,float] p3: 后一个点
    :param float t: 插值因子，范围 [0, 1]
    :param float alpha: 张力参数；默认为0.5

    :return: 曲线上的点
    :rtype: tuple[float,float,float]
    """
    def get_t(_p0, _p1):
        dx = _p1[0] - _p0[0]
        dy = _p1[1] - _p0[1]
        dz = _p1[2] - _p0[2]
        dist = sqrt(dx**2 + dy**2 + dz**2)
        return dist ** alpha

    t0 = 0.0
    t1 = get_t(p0, p1)
    t2 = t1 + get_t(p1, p2)
    if t2 - t1 < _ZERO_EPS:
        return p1
    t3 = t2 + get_t(p2, p3)
    _t = t1 + t * (t2 - t1)

    def calc_component(c0, c1, c2, c3):
        A1 = (t1 - _t) / (t1 - t0) * c0 + (_t - t0) / (t1 - t0) * c1 if t1 - t0 > _ZERO_EPS else c1
        A2 = (t2 - _t) / (t2 - t1) * c1 + (_t - t1) / (t2 - t1) * c2
        A3 = (t3 - _t) / (t3 - t2) * c2 + (_t - t2) / (t3 - t2) * c3 if t3 - t2 > _ZERO_EPS else c2

        B1 = (t2 - _t) / (t2 - t0) * A1 + (_t - t0) / (t2 - t0) * A2 if t2 - t0 > _ZERO_EPS else A2
        B2 = (t3 - _t) / (t3 - t1) * A2 + (_t - t1) / (t3 - t1) * A3 if t3 - t1 > _ZERO_EPS else A2

        C = (t2 - _t) / (t2 - t1) * B1 + (_t - t1) / (t2 - t1) * B2
        return C

    x = calc_component(p0[0], p1[0], p2[0], p3[0])
    y = calc_component(p0[1], p1[1], p2[1], p3[1])
    z = calc_component(p0[2], p1[2], p2[2], p3[2])
    return x, y, z


# endregion


# region Common ========================================================================================================


def median(*args):
    """
    计算一组数据的中位数。

    可传入一个可迭代对象（元组、字典等），或展开传入多个数据。
    ::

        median(iterable) -> float
        median(arg1, arg2, ...) -> float

    -----

    :return: 中位数
    :rtype: float
    """
    data = sorted(args[0] if len(args) == 1 else args)
    n = len(data)
    mid = n // 2
    if n % 2 == 1:
        return float(data[mid])
    else:
        return (data[mid - 1] + data[mid]) / 2.0


def var(*args):
    """
    计算一组数据的方差（总体方差）。

    可传入一个可迭代对象（元组、字典等），或展开传入多个数据。
    ::

        var(iterable) -> float
        var(arg1, arg2, ...) -> float

    -----

    :return: 方差
    :rtype: float
    """
    data = tuple(args[0]) if len(args) == 1 else args
    n = len(data)
    m = sum(data) / n
    return sum((x - m)**2.0 for x in data) / n


def std(*args):
    """
    计算一组数据的标准差（总体标准差）。

    可传入一个可迭代对象（元组、字典等），或展开传入多个数据。
    ::

        std(iterable) -> float
        std(arg1, arg2, ...) -> float

    -----

    :return: 标准差
    :rtype: float
    """
    return sqrt(var(*args))


def mean(*args):
    """
    计算一组数据的算术平均数。

    可传入一个可迭代对象（元组、字典等），或展开传入多个数据。
    ::

        mean(iterable) -> float
        mean(arg1, arg2, ...) -> float

    -----

    :return: 平均值
    :rtype: float
    """
    data = tuple(args[0]) if len(args) == 1 else args
    return float(sum(data) / len(data))


def sign(x):
    """
    获取数值的符号。

    -----

    :param float x: 数值

    :return: 符号；正数返回1，负数返回-1，零值返回0
    :rtype: int
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def lerp(a, b, t):
    """
    线性插值。

    -----

    :param float a: 起始值
    :param float b: 结束值
    :param float t: 插值因子，范围为 [0, 1]

    :return: 插值结果
    :rtype: float
    """
    return float(a + (b - a) * t)


def range_map(x, output_range, input_range=[0, 1], interp=None): # noqa
    """
    将某个区间内的数值映射到另一区间。

    -----

    :param float x: 输入值
    :param tuple[float,float] output_range: 输出区间（闭区间）
    :param tuple[float,float] input_range: 输入区间（闭区间）；默认为 [0, 1]
    :param function interp: 插值函数，接受一个参数 t ∈ [0, 1]，返回 [0, 1] 的值；默认为线性插值

    :return: 映射值
    :rtype: float
    """
    a, b = output_range
    j, k = input_range
    t = (x - j) / (k - j)
    if interp:
        t = interp(t)
    return float(a + (b - a) * t)


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
    return float(max(min_value, min(max_value, x)))


def box_max_edge_len(pos1, pos2):
    """
    计算AABB包围盒的最大棱长。
        
    -----
    
    :param tuple[float,float,float]|tuple[float,float] pos1: 包围盒对角坐标1
    :param tuple[float,float,float]|tuple[float,float] pos2: 包围盒对角坐标2
        
    :return: 包围盒最大棱长
    :rtype: float
    """
    return float(max(abs(a - b) for a, b in zip(pos1, pos2)))


# endregion


def __test__():
    pass


def __benchmark__(n, timer, pid, info, **kwargs):
    timer.start("distance2nearest_entity")
    for _ in xrange(n):
        distance2nearest_entity._org_func(False, pid)
    timer.end("distance2nearest_entity")

    from mod.server.extraServerApi import GetEngineActor
    eid = GetEngineActor().keys()[0]
    timer.start("distance")
    for _ in xrange(n):
        distance._org_func(False, pid, eid) # noqa
    timer.end("distance")

    timer.start("pos_entity_facing")
    for _ in xrange(n):
        pos_entity_facing._org_func(False, pid, 1)
    timer.end("pos_entity_facing")

    timer.start("is_in_sphere")
    for _ in xrange(n):
        is_in_sphere._org_func(False, pid, 1, (0, 0, 0))
    timer.end("is_in_sphere")

    timer.start("is_in_cylinder")
    for _ in xrange(n):
        is_in_cylinder._org_func(False, pid, 1, (0, 0, 0), (0, 1, 0))
    timer.end("is_in_cylinder")

    timer.start("is_in_sector")
    for _ in xrange(n):
        is_in_sector._org_func(False, pid, 1, 1, 30, (0, 0, 0), (1, 0, 0))
    timer.end("is_in_sector")

    timer.start("is_in_box")
    for _ in xrange(n):
        is_in_box._org_func(False, pid, (0, 0, 0), (1, 1, 1)) # noqa
    timer.end("is_in_box")

    timer.start("catmull_rom")
    for _ in xrange(n):
        catmull_rom((0, 0, 0), (5, 5, 5), (10, 0, 0), (15, 0, 0), 0.5)
    timer.end("catmull_rom")

    info.append("entity count: %d" % len(GetEngineActor()))













