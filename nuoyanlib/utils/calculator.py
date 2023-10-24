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
#   Last Modified : 2023-10-05
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
)
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi
from mod.common.utils.mcmath import Vector3 as _Vector3


__all__ = [
    'pos_distance_to_line',
    'floor_pos',
    'pos_distance',
    'to_relative_pos',
    'to_screen_pos',
    'rotate_pos',
    'straight_pos_list',
    'midpoint',
    'camera_rot_p2p',
    'circle_pos_list',
    'pos_entity_facing',
    'pos_forward_rot',
    'n_quantiles_index_list',
    'cube_center',
    'cube_longest_side_len',
    'is_in_sector',
    'sphere_pos_list',
    'cube_pos_list',
    'spiral_pos_list',
    'is_in_cube',
    'rot_diff',
    'ray_aabb_intersection',
]


def pos_distance_to_line(pos, linePos1, linePos2):
    """
    计算指定坐标pos与指定直线的距离。

    -----

    :param tuple[float,float,float] pos: 指定坐标
    :param tuple[float,float,float] linePos1: 指定直线上的坐标1
    :param tuple[float,float,float] linePos2: 指定直线上的坐标2
        
    :return: pos与指定直线的距离
    :rtype: float
    """
    a = pos_distance(pos, linePos1)
    b = pos_distance(pos, linePos2)
    c = pos_distance(linePos1, linePos2)
    p = (a + b + c) / 2
    s = _sqrt(p * (p - a) * (p - b) * (p - c)) # 海伦公式
    h = s / c * 2
    return h


def _is_client():
    return _clientApi.GetLocalPlayerId() != '-1'


def _get_comp_factory():
    return _clientApi.GetEngineCompFactory() if _is_client() else _serverApi.GetEngineCompFactory()


def floor_pos(pos):
    """
    对坐标进行向下取整。
        
    -----
    
    :param tuple[float,float,float] pos: 坐标
        
    :return: 取整后的坐标
    :rtype: tuple[int, int, int] 
    """
    return map(lambda x: int(_floor(x)), pos)


def pos_distance(firstPoint, secondPoint):
    """
    计算两个坐标间的距离。支持多元坐标。
        
    -----
    
    :param tuple[float, ...] firstPoint: 坐标1
    :param tuple[float, ...] secondPoint: 坐标2
        
    :return: 距离
    :rtype: float
    """
    if not firstPoint or not secondPoint:
        return -1.0
    return _sqrt(sum((a - b) ** 2 for a, b in zip(firstPoint, secondPoint)))


def to_relative_pos(entityPos1, entityPos2):
    """
    将实体1的绝对坐标转换为相对实体2的坐标。

    -----

    【示例】

    >>> to_relative_pos((1, 1, 4), (5, 1, 4))
    (-4, 0, 0)
        
    -----
    
    :param tuple[float,float,float] entityPos1: 实体1坐标
    :param tuple[float,float,float] entityPos2: 实体2坐标
        
    :return: 相对坐标
    :rtype: tuple[float,float,float]|None
    """
    if not entityPos1 or not entityPos2:
        return
    return tuple(a - b for a, b in zip(entityPos1, entityPos2))


def to_screen_pos(entityPos, centerPos, screenSize, maxDistance, uiSize, playerRot):
    """
    将实体的世界坐标转换为屏幕上的平面坐标，并根据玩家水平视角做对应旋转。可用于在小地图上显示实体图标。
        
    -----
    
    :param tuple[float,float,float] entityPos: 实体坐标
    :param tuple[float,float,float] centerPos: 屏幕坐标系原点对应的世界坐标（一般为玩家坐标）
    :param int screenSize: 屏幕上用于显示实体位置的正方形区域的边长（如小地图的尺寸）
    :param int maxDistance: 当实体位于上述区域的边界时，实体与centerPos之间的距离（如小地图的最远绘制距离）
    :param int uiSize: 实体图标ui尺寸
    :param float playerRot: 玩家水平视角
        
    :return: 屏幕坐标
    :rtype: tuple[float, float]|None
    """
    if not entityPos or not centerPos or not playerRot:
        return
    relativePos = to_relative_pos(centerPos, entityPos)
    halfScreenSize = screenSize / 2.0
    halfUiSize = uiSize / 2.0
    ratio = (relativePos[0] / maxDistance, relativePos[2] / maxDistance)
    origPos = (halfScreenSize * ratio[0], halfScreenSize * ratio[1])
    rotatePos = rotate_pos(playerRot, origPos)
    screenPos = (
        halfScreenSize - rotatePos[0] - halfUiSize,
        halfScreenSize - rotatePos[1] - halfUiSize,
    )
    return screenPos


def rotate_pos(angle, pos):
    """
    计算给定坐标绕坐标原点旋转后的新坐标。
        
    -----
    
    :param float angle: 旋转角
    :param tuple[float, float] pos: 原始坐标（二维坐标）
        
    :return: 旋转后的坐标
    :rtype: tuple[float, float]|None
    """
    if not angle or not pos:
        return
    radian = (-angle / 180) * _pi
    rotateX = _cos(radian) * pos[0] - _sin(radian) * pos[1]
    rotateY = _cos(radian) * pos[1] + _sin(radian) * pos[0]
    return rotateX, rotateY


def straight_pos_list(pos1, pos2, count, only=-1):
    """
    计算给定两点连线上各点的坐标(不包括pos1和pos2)。
        
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
    xStep = xd / (count + 1)
    yStep = yd / (count + 1)
    zStep = zd / (count + 1)
    result = []
    if only != -1:
        count = only
    while count > 0:
        result.append((pos2[0] + xStep * count, pos2[1] + yStep * count, pos2[2] + zStep * count))
        count -= 1
    return result


def midpoint(firstPoint, secondPoint):
    """
    计算给定两点间的中点坐标。
        
    -----
    
    :param tuple[float, ...] firstPoint: 坐标1
    :param tuple[float, ...] secondPoint: 坐标2
        
    :return: 中点坐标
    :rtype: tuple[float, ...]|None
    """
    if not firstPoint or not secondPoint:
        return
    midpos = []
    for i in range(len(firstPoint)):
        midpos.append((firstPoint[i] + secondPoint[i]) / 2)
    return tuple(midpos)


def camera_rot_p2p(pos1, pos2):
    """
    计算从pos1指向pos2的相机角度。（可用于将玩家相机视角锁定到某一坐标）

    -----

    :param tuple[float,float,float] pos1: 坐标1
    :param tuple[float,float,float] pos2: 坐标2

    :return: (竖直角度, 水平角度)
    :rtype: tuple[float, float]|None
    """
    if not pos1 or not pos2:
        return
    x = pos2[0] - pos1[0]
    if x == 0:
        x = 0.000000001
    y = pos2[1] - pos1[1]
    z = pos2[2] - pos1[2]
    horiDis = pos_distance((pos2[0], pos2[2]), (pos1[0], pos1[2]))
    if horiDis == 0:
        horiDis = 0.000000001
    horizontalRot = 90 + (_atan(z / x) / _pi) * 180 + (-180 if x > 0 else 0)
    verticalRot = -(_atan(y / horiDis) / _pi) * 180
    return verticalRot, horizontalRot


def circle_pos_list(centerPos, radius, density):
    """
    计算以某一坐标为圆心的圆上各点的坐标。

    -----

    :param tuple[float,float,float] centerPos: 圆心坐标
    :param float radius: 半径
    :param int density: 返回的坐标个数

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    if not centerPos:
        return []
    result = []
    step = (2 * _pi) / density
    ox, oy, oz = centerPos
    for i in range(density):
        angle = i * step
        nx = radius * _sin(angle) + ox
        nz = radius * _cos(angle) + oz
        result.append((nx, oy, nz))
    return result


def pos_entity_facing(entityId, dis, use0Yaw=False, heightOffset=0.0):
    """
    计算实体视角方向上、给定距离上的位置的坐标。

    -----

    :param str entityId: 实体ID
    :param float dis: 距离
    :param bool use0Yaw: 是否使用0作为实体竖直方向上的视角
    :param float heightOffset: 高度偏移量（如实体为玩家建议使用1.6，其他实体建议使用其头部到脚底的距离）

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    compFactory = _get_comp_factory()
    rot = compFactory.CreateRot(entityId).GetRot()
    if not rot:
        return
    if use0Yaw:
        rot = (0, rot[1])
    dirRot = _clientApi.GetDirFromRot(rot) if _is_client() else _serverApi.GetDirFromRot(rot)
    ep = compFactory.CreatePos(entityId).GetFootPos()
    if not ep:
        return
    ep = (ep[0], ep[1] + heightOffset, ep[2])
    result = tuple(ep[i] + dirRot[i] * dis for i in range(3))
    return result


def pos_forward_rot(pos, rot, dis):
    """
    计算从pos射出，以rot为方向的射线上，与pos的距离为dis的位置的坐标。

    -----

    :param tuple[float,float,float] pos: 坐标
    :param tuple[float, float] rot: (竖直角度, 水平角度)
    :param float dis: 距离

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not rot or not pos:
        return
    dirRot = _clientApi.GetDirFromRot(rot) if _is_client() else _serverApi.GetDirFromRot(rot)
    resultPos = tuple(pos[i] + dirRot[i] * dis for i in range(3))
    return resultPos


def n_quantiles_index_list(n, data):
    """
    计算一串数据的n分位数的位置。

    -----

    【示例】

    >>> n_quantiles_index_list(4, range(11))
    [2, 5, 8]

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


def cube_center(startPos, endPos):
    """
    计算立方体中心坐标。

    -----

    :param tuple[float,float,float] startPos: 立方体对角顶点坐标1
    :param tuple[float,float,float] endPos: 立方体对角顶点坐标2

    :return: 中心坐标
    :rtype: tuple[float,float,float]|None
    """
    if not startPos or not endPos:
        return
    x = (startPos[0] + endPos[0]) / 2.0
    y = (startPos[1] + endPos[1]) / 2.0
    z = (startPos[2] + endPos[2]) / 2.0
    return x, y, z


def cube_longest_side_len(startPos, endPos):
    """
    计算立方体最大棱长。
        
    -----
    
    :param tuple[float,float,float] startPos: 立方体对角顶点坐标1
    :param tuple[float,float,float] endPos: 立方体对角顶点坐标2
        
    :return: 最大棱长
    :rtype: float
    """
    if not startPos or not endPos:
        return -1.0
    xl = abs(startPos[0] - endPos[0])
    yl = abs(startPos[1] - endPos[1])
    zl = abs(startPos[2] - endPos[2])
    return max(xl, yl, zl)


def is_in_sector(testPos, vertexPos, radius, sectorAngle, sectorBisectorAngle):
    """
    判断给定坐标是否在扇形区域内。
        
    -----
    
    :param tuple[float,float,float] testPos: 待测试的坐标
    :param tuple[float,float,float] vertexPos: 扇形顶点坐标
    :param float radius: 扇形半径
    :param float sectorAngle: 扇形张开的角度(<=180)
    :param float sectorBisectorAngle: 扇形角平分线所在直线的水平角度
        
    :return: 在扇形区域内则返回True，否则返回False
    :rtype: bool
    """
    dis = pos_distance(vertexPos, testPos)
    if dis <= radius:
        if sectorAngle > 180:
            sectorAngle = 180
        elif sectorAngle < 0:
            sectorAngle = 0
        dx = testPos[0] - vertexPos[0]
        dz = testPos[2] - vertexPos[2]
        testPosAngle = -_degrees(_atan2(dx, dz))
        minAngle = sectorBisectorAngle - sectorAngle / 2
        maxAngle = sectorBisectorAngle + sectorAngle / 2
        rangeList = []
        if sectorBisectorAngle < 0:
            if minAngle < -180:
                rangeList.append((-180, maxAngle))
                rangeList.append((360 - abs(minAngle), 180))
            else:
                rangeList.append((minAngle, maxAngle))
        else:
            if maxAngle > 180:
                rangeList.append((minAngle, 180))
                rangeList.append((-180, -360 + maxAngle))
            else:
                rangeList.append((minAngle, maxAngle))
        for r in rangeList:
            if r[0] <= testPosAngle <= r[1]:
                return True
    return False


def sphere_pos_list(centerPos, radius, density):
    """
    根据球心、半径计算球面上各点的坐标。
        
    -----
    
    :param tuple[float,float,float] centerPos: 球心坐标
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
            x = centerPos[0] + radius * _sin(a) * _cos(b)
            y = centerPos[1] + radius * _sin(a) * _sin(b)
            z = centerPos[2] + radius * _cos(a)
            result.append((x, y, z))
            b += step2
        a += step1
        b = 0
    return result


def cube_pos_list(pos1, pos2, step=1):
    """
    计算立方体区域内各点的坐标。
        
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


def spiral_pos_list(startPos, iterations):
    """
    生成螺旋轨迹坐标列表。

    -----

    :param tuple[float,float,float] startPos: 开始坐标
    :param int iterations: 迭代次数

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    res = []
    axis = 0
    relPos = [0, 0]
    initStep = step = 1
    for i in range(iterations):
        if i > 0:
            if axis == 0:
                relPos[0] += 1
            elif axis == 1:
                relPos[1] -= 1
            elif axis == 2:
                relPos[0] -= 1
            else:
                relPos[1] += 1
            step -= 1
            if step <= 0:
                axis = (axis + 1) % 4
                if axis == 0 or axis == 2:
                    initStep += 1
                step = initStep
        res.append((startPos[0] + relPos[0], startPos[1], startPos[2] + relPos[1]))
    return res


def is_in_cube(obj, pos1, pos2, ignoreY=False):
    """
    判断对象是否在立方体区域内。
        
    -----
    
    :param str|tuple[float,float,float] obj: 实体ID或坐标
    :param tuple[float,float,float] pos1: 立方体对角顶点坐标1
    :param tuple[float,float,float] pos2: 立方体对角顶点坐标2
    :param bool ignoreY: 是否忽略Y轴
        
    :return: 在立方体区域内返回True，否则返回False
    :rtype: bool
    """
    if isinstance(obj, str):
        targetPos = _get_comp_factory().CreatePos(obj).GetFootPos()
    else:
        targetPos = obj
    if not targetPos or not pos1 or not pos2:
        return False
    def numInRange(num, r1, r2):
        return r1 <= num <= r2 or r2 <= num <= r1
    for i in range(3):
        if ignoreY and i == 1:
            continue
        if not numInRange(targetPos[i], pos1[i], pos2[i]):
            return False
    return True


def rot_diff(r1, r2):
    """
    计算两个角度之间的实际差值。
    
    -----
    
    【示例】
    
    >>> rot_diff(-170, 20) 
    170
        
    -----
    
    :param float r1: 角度1
    :param float r2: 角度2
        
    :return: 差值（0~180）
    :rtype: float
    """
    diff = r1 - r2
    if diff < -180:
        diff += 360
    elif diff >= 180:
        diff -= 360
    return abs(diff)


def ray_aabb_intersection(rayStartPos, rayDir, length, cubeCenterPos, cubeSize):
    """
    从指定位置射出一条射线，计算该射线与指定立方体（AABB）的第一个交点坐标，不相交时返回None。

    -----

    :param tuple[float,float,float] rayStartPos: 射线起始坐标
    :param tuple[float,float,float] rayDir: 射线方向向量（单位向量）
    :param float length: 射线长度
    :param tuple[float,float,float] cubeCenterPos: 立方体中心坐标
    :param tuple[float,float,float] cubeSize: 立方体边长元组，分别对应xyz上的边长

    :return: 射线与立方体的第一个交点坐标，不相交时返回None
    :rtype: tuple[float,float,float]|None
    """
    rayStartPos = _Vector3(rayStartPos)
    rayDir = _Vector3(rayDir)
    cubeCenterPos = _Vector3(cubeCenterPos)
    localStartPos = rayStartPos - cubeCenterPos
    tMin = -float('inf')
    tMax = float('inf')
    for i in range(3):
        if rayDir[i] == 0.0:
            continue
        t1 = (cubeSize[i] / 4.0 - localStartPos[i]) / rayDir[i]
        t2 = (-cubeSize[i] / 4.0 - localStartPos[i]) / rayDir[i]
        tMin = max(tMin, min(t1, t2))
        tMax = min(tMax, max(t1, t2))
    if 0.0 <= tMin <= tMax and tMin <= length:
        return (rayStartPos + rayDir * tMin).ToTuple()


_LEVEL_ID = _serverApi.GetLevelId() or _clientApi.GetLevelId()


def get_blocks_by_ray(startPos, direction, length, dimension=0, count=0, filterBlocks=None):
    """
    从指定位置射出一条射线，获取该射线经过的方块。

    返回一个列表，方块按照由近到远的顺序排列，列表每个元素为一个字典，结构如下：

    >>> {
    ...     "name": str, # 方块ID
    ...     "aux": int, # 方块特殊值
    ...     "pos": Tuple[float, float, float], # 方块坐标
    ...     "intersection": Tuple[float, float, float], # 射线与方块的第一个交点的坐标
    ... }

    -----

    *算法作者：头脑风暴*

    *修改：* `诺言Nuoyan <https://gitee.com/charming-lee>`_

    -----

    :param tuple[float,float,float] startPos: 射线起始坐标
    :param tuple[float,float,float] direction: 射线方向向量
    :param float length: 射线长度
    :param int dimension: 维度ID，默认为0
    :param int count: 获取到多少个方块后停止，默认为0，表示不限制数量
    :param list[str] filterBlocks: 过滤的方块ID列表，默认过滤空气

    :return: 射线经过的方块的列表，顺序为由近到远，列表每个元素为一个字典，字典结构请见上方
    :rtype: list[dict[str, str|int|tuple]]
    """
    if filterBlocks is None:
        filterBlocks = ['minecraft:air']
    tList = [0]
    for n in range(3):
        s = startPos[n]
        d = direction[n]
        if d == 0:
            continue
        start = int(_floor(s))
        end = int(_floor(s + d * length))
        stepRange = range(start + 1, end + 1) if d > 0 else range(start, end, -1)
        for i in stepRange:
            tList.append((i - s) / d)
    tList.sort()
    tList = tList[:-1]
    comp = _get_comp_factory().CreateBlockInfo(_LEVEL_ID)
    blockList = []
    for t in tList:
        blockPos = [0, 0, 0]
        intersection = [0, 0, 0]
        for n in range(3):
            posVal = startPos[n] + t * direction[n]
            intersection[n] = posVal
            if posVal.is_integer() and direction[n] < 0:
                posVal -= 1
            blockPos[n] = int(_floor(posVal))
        blockPos = tuple(blockPos)
        block = comp.GetBlockNew(blockPos, dimension)
        if block and block['name'] not in filterBlocks:
            blockList.append({
                'name': block['name'],
                'aux': block['aux'],
                'pos': blockPos,
                'intersection': intersection,
            })
            if len(blockList) >= count > 0:
                break
    return blockList















