# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
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


from random import uniform as _uniform, Random as _Random, randint as _randint
from string import digits as _digits, ascii_lowercase as _ascii_lowercase, ascii_uppercase as _ascii_uppercase
from calculator import pos_distance as _pos_distance
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi


__all__ = [
    "random_pos",
    "random_string",
    "random_even_poses",
]


def _is_client():
    return _clientApi.GetLocalPlayerId() != "-1"


def random_pos(centerPos, grid, useTopBlockHeight=False, dimension=0):
    # type: (tuple[float, float, float], float, bool, int) -> tuple[float, float, float] | None
    """
    在指定区域内随机获取一点坐标。
    -----------------------------------------------------------
    【centerPos: Tuple[float, float, float]】 区域中心坐标
    【grid: float】 区域半径
    【useTopBlockHeight: bool = False】 是否以最高的非空气方块的高度作为返回坐标的Y值（只适用于服务端）
    【dimension: int = 0】 维度
    -----------------------------------------------------------
    return: Optional[Tuple[float, float, float]] -> 坐标
    """
    if not centerPos:
        return
    ranX = _randint(-grid, grid)
    ranZ = _randint(-grid, grid)
    x = centerPos[0] + ranX
    z = centerPos[2] + ranZ
    if useTopBlockHeight and not _is_client():
        compFactory = _serverApi.GetEngineCompFactory()
        levelId = _serverApi.GetLevelId()
        y = compFactory.CreateBlockInfo(levelId).GetTopBlockHeight((x, z), dimension)
        if y is not None:
            return x, y, z
        else:
            return None
    else:
        ranY = _randint(-grid, grid)
        y = centerPos[1] + ranY
        return x, y, z


def _gen_str(choice, s, l):
    return "".join(choice(s) for _ in range(l))


_random_ins = {}


def random_string(length, lower=True, upper=True, num=True, seed=None, generateNum=1):
    # type: (int, bool, bool, bool, ..., int) -> str | list[str]
    """
    生成随机字符串。
    -----------------------------------------------------------
    【length: int】 生成的字符串长度
    【lower: bool = True】 是否包含小写字母
    【upper: bool = True】 是否包含大写字母
    【num: bool = True】 是否包含数字
    【seed: Any = None】 随机数种子
    【generateNum: int = 1】 生成数量，默认为1，大于1时将以列表返回
    -----------------------------------------------------------
    return: Union[str, List[str]] -> 随机字符串
    """
    s = (_ascii_lowercase if lower else "") + (_ascii_uppercase if upper else "") + (_digits if num else "")
    random = _random_ins.setdefault(seed, _Random(seed))
    if generateNum == 1:
        return _gen_str(random.choice, s, length)
    else:
        return [_gen_str(random.choice, s, length) for _ in range(generateNum)]


def _is_pos_far_enough(poses, x, y, z, minDistance):
    for pos in poses:
        if _pos_distance(pos, (x, y, z)) < minDistance:
            return False
    return True


def random_even_poses(centerPos, xRange, yRange, zRange, posNum, minDistance=1.0):
    # type: (tuple[float, float, float], float, float, float, int, float) -> list[tuple[float, float, float]]
    """
    在指定坐标周围，生成随机的均匀分布的多个坐标。
    -----------------------------------------------------------
    【centerPos: Tuple[float, float, float]】 中心坐标
    【xRange: float】 x坐标的取值范围
    【yRange: float】 y坐标的取值范围
    【zRange: float】 z坐标的取值范围
    【posNum: int】 生成的坐标数量
    【minDistance: float = 1.0】 生成的坐标之间的最小距离，越小生成的坐标越不均匀
    -----------------------------------------------------------
    return: List[Tuple[float, float, float]] -> 坐标列表
    """
    poses = []
    while len(poses) < posNum:
        x = centerPos[0] + _uniform(-xRange, xRange)
        y = centerPos[1] + _uniform(-yRange, yRange)
        z = centerPos[2] + _uniform(-zRange, zRange)
        if not poses or _is_pos_far_enough(poses, x, y, z, minDistance):
            poses.append((x, y, z))
    return poses


def _test():
    print random_string(20, lower=False)
    print random_string(20, upper=False)
    print random_string(20, num=False)
    print random_string(20, num=False, seed=20230315, generateNum=5)
    for i in range(5):
        print random_string(20, num=False, seed=20230315)


if __name__ == "__main__":
    _test()

























