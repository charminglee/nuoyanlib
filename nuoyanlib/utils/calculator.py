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
#   Last Modified : 2023-07-03
#
# ====================================================


from collections import Sequence as _Sequence
from random import randint as _randint
from math import atan as _atan, degrees as _degrees, atan2 as _atan2, sqrt as _sqrt, pi as _pi, sin as _sin, \
    cos as _cos, fmod as _fmod, floor as _floor
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi


__all__ = [
    "pos_distance_to_line",
    "floor_pos",
    "pos_distance",
    "to_relative_pos",
    "to_screen_pos",
    "rotate_pos",
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
    "perlin_noise",
    "rot_diff",
]


def pos_distance_to_line(pos1, pos2, pos3):
    # type: (tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]) -> float
    """
    计算pos1到pos2和pos3的连线的距离。
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 要计算距离的坐标
    【pos2: Tuple[float, float, float]】 连线上的坐标1
    【pos3: Tuple[float, float, float]】 连线上的坐标2
    -----------------------------------------------------------
    return: float -> pos1到pos2和pos3的连线的距离
    """
    a = pos_distance(pos1, pos2)
    b = pos_distance(pos1, pos3)
    c = pos_distance(pos2, pos3)
    p = (a + b + c) / 2
    s = _sqrt(p * (p - a) * (p - b) * (p - c))
    h = s / c * 2
    return h


def _is_client():
    return _clientApi.GetLocalPlayerId() != "-1"


def _get_comp_factory():
    return _clientApi.GetEngineCompFactory() if _is_client() else _serverApi.GetEngineCompFactory()


def floor_pos(pos):
    # type: (tuple[float, float, float]) -> tuple[int, int, int]
    """
    对坐标进行向下取整。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 坐标
    -----------------------------------------------------------
    return: Tuple[int, int, int] -> 取整后的坐标
    """
    return tuple(int(_floor(p)) for p in pos)


def pos_distance(firstPoint, secondPoint):
    # type: (tuple[float, ...], tuple[float, ...]) -> float
    """
    计算两个坐标间的距离。支持多元坐标。
    -----------------------------------------------------------
    【firstPoint: Tuple[float, ...]】 坐标1
    【secondPoint: Tuple[float, ...]】 坐标2
    -----------------------------------------------------------
    return: float -> 距离
    """
    if not firstPoint or not secondPoint:
        return -1.0
    return _sqrt(sum((firstPoint[i] - secondPoint[i])**2 for i in range(len(firstPoint))))


def to_relative_pos(entityPos1, entityPos2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float, float] | None
    """
    将实体1的绝对坐标转换为相对实体2的坐标。
    【示例】
    to_relative_pos((1, 1, 4), (5, 1, 4))     # (-4, 0, 0)
    -----------------------------------------------------------
    【entityPos1: Tuple[float, float, float]】 实体1坐标
    【entityPos2: Tuple[float, float, float]】 实体2坐标
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 相对坐标
    """
    if not entityPos1 or not entityPos2:
        return
    relativePos = (
        entityPos1[0] - entityPos2[0],
        entityPos1[1] - entityPos2[1],
        entityPos1[2] - entityPos2[2]
    )
    return relativePos


def to_screen_pos(entityPos, centerPos, screenSize, maxDistance, uiSize=0, playerRot=0.0):
    # type: (tuple[float, float, float], tuple[float, float, float], int, int, int, float) -> tuple[float, float] | None
    """
    将实体的世界坐标转换为屏幕上的平面坐标，并根据玩家水平视角做对应旋转。可用于在小地图上显示实体图标。
    -----------------------------------------------------------
    【entityPos: Tuple[float, float, float]】 实体坐标
    【centerPos: Tuple[float, float, float]】 屏幕坐标系原点对应的世界坐标（一般为玩家坐标）
    【screenSize: int】 屏幕上用于显示实体位置的正方形区域的边长（如小地图的尺寸）
    【maxDistance: int】 当实体位于上述区域的边界时，实体与centerPos之间的距离（如小地图的最远绘制距离）
    【uiSize: int = 0】 实体图标ui尺寸
    【playerRot: float = 0.0】 玩家水平视角
    -----------------------------------------------------------
    return: Optional[Tuple[float, float]] -> 屏幕坐标
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
        halfScreenSize - rotatePos[1] - halfUiSize
    )
    return screenPos


def rotate_pos(angle, pos):
    # type: (float, tuple[float, float]) -> tuple[float, float] | None
    """
    计算给定坐标绕坐标原点旋转后的新坐标。
    -----------------------------------------------------------
    【angle: float】 旋转角
    【pos: Tuple[float, float]】 原始坐标（平面坐标）
    -----------------------------------------------------------
    return: Optional[Tuple[float, float]] -> 旋转后的坐标
    """
    if not angle or not pos:
        return
    radian = (-angle / 180) * _pi
    rotateX = _cos(radian) * pos[0] - _sin(radian) * pos[1]
    rotateY = _cos(radian) * pos[1] + _sin(radian) * pos[0]
    return rotateX, rotateY


def straight_pos_list(pos1, pos2, count, only=-1):
    # type: (tuple[float, float, float], tuple[float, float, float], int, int) -> list[tuple[float, float, float]]
    """
    计算给定两点连线上各点的坐标(不包括pos1和pos2)。
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 坐标1
    【pos2: Tuple[float, float, float]】 坐标2
    【count: int】 返回的坐标的个数
    【only: int = -1】 只取前only个点，-1表示取所有点
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标元组列表
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
    # type: (tuple[float, ...], tuple[float, ...]) -> tuple[float, ...] | None
    """
    计算给定两点间的中点坐标。
    -----------------------------------------------------------
    【firstPoint: Tuple[float, ...]】 坐标1
    【secondPoint: Tuple[float, ...]】 坐标2
    -----------------------------------------------------------
    return: Optional[Tuple[float, ...]] -> 中点坐标
    """
    if not firstPoint or not secondPoint:
        return
    midpos = []
    if len(firstPoint) == len(secondPoint):
        for i in range(len(firstPoint)):
            midpos.append((firstPoint[i] + secondPoint[i]) / 2)
        return tuple(midpos)


def camera_rot_p2p(pos1, pos2):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float] | None
    """
    计算从pos1指向pos2的相机角度。（可用于将玩家相机视角锁定到某一坐标）
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 坐标1
    【pos2: Tuple[float, float, float]】 坐标2
    -----------------------------------------------------------
    return: Optional[Tuple[float, float]] -> 竖直角度, 水平角度
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
    # type: (tuple[float, float, float], float, int) -> list[tuple[float, float, float]]
    """
    计算以某一坐标为圆心的圆上各点的坐标。
    -----------------------------------------------------------
    【centerPos: Tuple[float, float, float]】 圆心坐标
    【radius: float】 半径
    【density: int】 返回的坐标个数
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标列表
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
    # type: (str, float, bool, float) -> tuple[float, float, float] | None
    """
    计算实体视角方向上、给定距离上的位置的坐标。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【dis: float】 距离
    【use0Yaw: bool = False】 是否使用0作为实体竖直方向上的视角
    【heightOffset: float = 0.0】 高度偏移量（如实体为玩家建议使用1.6，其他实体建议使用其头部到脚底的距离）
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 坐标
    """
    compFactory = _get_comp_factory()
    rot = compFactory.CreateRot(entityId).GetRot()
    if not rot:
        return
    if use0Yaw:
        rot = (0, rot[1])
    dirRot = _clientApi.GetDirFromRot(rot) if _is_client() else _serverApi.GetDirFromRot(rot)
    ep = compFactory.CreatePos(entityId).GetFootPos()
    ep = (ep[0], ep[1] + heightOffset, ep[2])
    result = tuple(ep[i] + dirRot[i] * dis for i in range(3))
    return result


def pos_forward_rot(pos, rot, dis):
    # type: (tuple[float, float, float], tuple[float, float], float) -> tuple[float, float, float] | None
    """
    计算从pos射出，以rot为方向的射线上，与pos的距离为dis的位置的坐标。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 坐标
    【rot: Tuple[float, float]】 (竖直角度, 水平角度)
    【dis: float】 距离
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 坐标
    """
    if not rot or not pos:
        return
    dirRot = _clientApi.GetDirFromRot(rot) if _is_client() else _serverApi.GetDirFromRot(rot)
    resultPos = tuple(pos[i] + dirRot[i] * dis for i in range(3))
    return resultPos


def n_quantiles_index_list(n, data):
    # type: (int, _Sequence) -> list[int]
    """
    计算一串数据的n分位数的位置。
    【示例】
    n_quantiles_index_list(4, range(11))     # [2, 5, 8]
    -----------------------------------------------------------
    【n: int】 n分位
    【data: Sequence】 元组、列表、集合等
    -----------------------------------------------------------
    return: List[int] -> n分位数的位置列表
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
    # type: (tuple[float, float, float], tuple[float, float, float]) -> tuple[float, float, float] | None
    """
    计算立方体中心坐标。
    -----------------------------------------------------------
    【startPos: Tuple[float, float, float]】 立方体对角顶点坐标1
    【endPos: Tuple[float, float, float]】 立方体对角顶点坐标2
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 中心坐标
    """
    if not startPos or not endPos:
        return
    x = (startPos[0] + endPos[0]) / 2.0
    y = (startPos[1] + endPos[1]) / 2.0
    z = (startPos[2] + endPos[2]) / 2.0
    return x, y, z


def cube_longest_side_len(startPos, endPos):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> float
    """
    计算立方体最大棱长。
    -----------------------------------------------------------
    【startPos: Tuple[float, float, float]】 立方体对角顶点坐标1
    【endPos: Tuple[float, float, float]】 立方体对角顶点坐标2
    -----------------------------------------------------------
    return: float -> 最大棱长
    """
    if not startPos or not endPos:
        return -1.0
    xl = abs(startPos[0] - endPos[0])
    yl = abs(startPos[1] - endPos[1])
    zl = abs(startPos[2] - endPos[2])
    return max(xl, yl, zl)


def is_in_sector(testPos, vertexPos, radius, sectorAngle, sectorBisectorAngle):
    # type: (tuple[float, float, float], tuple[float, float, float], float, float, float) -> bool
    """
    判断给定坐标是否在扇形区域内。
    -----------------------------------------------------------
    【testPos: Tuple[float, float, float]】 待测试的坐标
    【vertexPos: Tuple[float, float, float]】 扇形顶点坐标
    【radius: float】 扇形半径
    【sectorAngle: float】 扇形张开的角度(<=180)
    【sectorBisectorAngle: float】 扇形角平分线所在直线的水平角度
    -----------------------------------------------------------
    return: bool -> 在扇形区域内则返回True，否则返回False
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
    # type: (tuple[float, float, float], float, int) -> list[tuple[float, float, float]]
    """
    根据球心、半径计算球面上各点的坐标。
    -----------------------------------------------------------
    【centerPos: Tuple[float, float, float]】 球心坐标
    【radius: float】 半径
    【density: int】 返回的坐标个数
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标列表
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
    # type: (tuple[float, float, float], tuple[float, float, float], int) -> list[tuple[float, float, float]]
    """
    计算立方体区域内各点的坐标。
    -----------------------------------------------------------
    【pos1: Tuple[float, float, float]】 立方体对角坐标1
    【pos2: Tuple[float, float, float]】 立方体对角坐标2
    【step: int = 1】 迭代步长
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标列表
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
    # type: (tuple[float, float, float], int) -> list[tuple[float, float, float]]
    """
    生成螺旋轨迹坐标列表。
    -----------------------------------------------------------
    【startPos: Tuple[float, float, float]】 开始坐标
    【iterations: int】 迭代次数
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标列表
    """
    pos = startPos
    result = [startPos]
    xOne, xZero, xSym = 1, 0, 1
    zOne, zZero, zSym = 0, 1, 1
    for i in range(1, iterations):
        xOff = 1 * xSym if xOne > 0 else 0
        zOff = 1 * zSym if zOne > 0 else 0
        pos = (pos[0] + xOff, pos[1], pos[2] + zOff)
        result.append(pos)
        xOne -= 1
        xZero -= 1
        if xOne == 0:
            xOne -= 1
            xZero = -xZero
        if xZero == 0:
            xOne = -xOne
            xSym *= -1
        zOne -= 1
        zZero -= 1
        if zOne == 0:
            zZero = -zZero
            zSym *= -1
        if zZero == 0:
            zZero -= 1
            zOne = -zOne
    return result


def is_in_cube(obj, pos1, pos2, ignoreY=False):
    # type: (str | tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], bool) -> bool
    """
    判断对象是否在立方体区域内。
    -----------------------------------------------------------
    【obj: Union[str, Tuple[float, float, float]]】 实体ID或坐标
    【pos1: Tuple[float, float, float]】 立方体对角顶点坐标1
    【pos2: Tuple[float, float, float]】 立方体对角顶点坐标2
    【ignoreY: bool = False】 是否忽略Y轴
    -----------------------------------------------------------
    return: bool -> 在立方体区域内返回True，否则返回False
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


def perlin_noise(x, y, z):
    # type: (float, float, float) -> float
    # 出处：https://blog.csdn.net/qq_41518277/article/details/82779516
    """
    柏林噪声算法。
    -----------------------------------------------------------
    【x: float】 x坐标
    【y: float】 y坐标
    【z: float】 z坐标
    -----------------------------------------------------------
    return: float -> -1~1的随机数
    """
    GRAD3 = (
        (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
        (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
        (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
        (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1)
    )
    permutation = (
        151, 160, 137, 91, 90, 15, 23, 66, 215, 61, 156, 180, 29, 24, 72, 243, 141, 128, 195, 78, 114,
        131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10,
        190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
        88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
        77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
        102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
        135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
        5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
        223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
        129, 22, 39, 253, 9, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
        251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
        49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
        138, 236, 205, 93, 222, 67
    )
    period = len(permutation)
    permutation *= 2
    perm = list(range(period))
    perm_right = period - 1
    for i in perm:
        j = _randint(0, perm_right)
        perm[i], perm[j] = perm[j], perm[i]
    permutation = tuple(perm) * 2
    i = int(_fmod(_floor(x), 127))
    j = int(_fmod(_floor(y), 127))
    k = int(_fmod(_floor(z), 127))
    ii = (i + 1) % 127
    jj = (j + 1) % 127
    kk = (k + 1) % 127
    x -= _floor(x)
    y -= _floor(y)
    z -= _floor(z)
    fx = x**3 * (x * (x * 6 - 15) + 10)
    fy = y**3 * (y * (y * 6 - 15) + 10)
    fz = z**3 * (z * (z * 6 - 15) + 10)
    A = permutation[i]
    AA = permutation[A + j]
    AB = permutation[A + jj]
    B = permutation[ii]
    BA = permutation[B + j]
    BB = permutation[B + jj]
    def lerp(t, a, b):
        return a + t*(b - a)
    def grad3(h, xx, yy, zz):
        g = GRAD3[h % 16]
        return xx*g[0] + yy*g[1] + zz*g[2]
    return lerp(
        fz,
        lerp(
            fy,
            lerp(fx, grad3(permutation[AA + k], x, y, z), grad3(permutation[BA + k], x - 1, y, z)),
            lerp(fx, grad3(permutation[AB + k], x, y - 1, z), grad3(permutation[BB + k], x - 1, y - 1, z))
        ),
        lerp(
            fy,
            lerp(fx, grad3(permutation[AA + kk], x, y, z - 1), grad3(permutation[BA + kk], x - 1, y, z - 1)),
            lerp(fx, grad3(permutation[AB + kk], x, y - 1, z - 1), grad3(permutation[BB + kk], x - 1, y - 1, z - 1))
        )
    )


def rot_diff(r1, r2):
    # type: (float, float) -> float
    """
    计算两个角度之间的实际差值。
    【示例】
    rot_diff(-170, 20)     # 170
    -----------------------------------------------------------
    【r1: float】 角度1
    【r2: float】 角度2
    -----------------------------------------------------------
    return: float -> 差值（0~180）
    """
    diff = r1 - r2
    if diff < -180:
        diff += 360
    elif diff >= 180:
        diff -= 360
    return abs(diff)














