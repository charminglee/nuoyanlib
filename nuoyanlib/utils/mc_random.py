# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-19
|
| ==============================================
"""


from math import pi, sin, cos
from random import uniform, Random
from string import digits, ascii_lowercase, ascii_uppercase
from .._core._sys import get_lv_comp, is_client
from .mc_math import pos_distance


__all__ = [
    "random_pos",
    "random_string",
    "random_even_poses",
]


def random_pos(center_pos, r, dim=0, use_top_height=False):
    """
    | 在指定区域内随机获取一点坐标。
    
    -----

    :param tuple[float,float,float] center_pos: 区域中心坐标
    :param float r: 区域半径
    :param int dim: 维度ID，若在客户端调用则使用客户端的维度ID；默认为0
    :param bool use_top_height: 是否以最高的非空气方块的高度作为返回坐标的Y值，默认为False

    :return: 坐标
    :rtype: tuple[float,float,float]|None
    """
    if not center_pos:
        return
    x = center_pos[0] + uniform(-r, r)
    z = center_pos[2] + uniform(-r, r)
    if use_top_height:
        if is_client():
            y = get_lv_comp().BlockInfo.GetTopBlockHeight((x, z))
        else:
            y = get_lv_comp().BlockInfo.GetTopBlockHeight((x, z), dim)
        if y is not None:
            return x, y, z
    else:
        y = center_pos[1] + uniform(-r, r)
        return x, y, z


def _gen_str(choice, s, l):
    return "".join(choice(s) for _ in range(l))


_random_ins = {}


def random_string(length, lower=True, upper=True, num=True, seed=None, generate_num=1):
    """
    | 生成随机字符串。
    
    -----

    :param int length: 生成的字符串长度
    :param bool lower: 是否包含小写字母，默认为是
    :param bool upper: 是否包含大写字母，默认为是
    :param bool num: 是否包含数字，默认为是
    :param Any seed: 随机数种子，默认为None
    :param int generate_num: 生成数量，默认为1，大于1时将以列表返回

    :return: 随机字符串
    :rtype: str|list[str]
    """
    s = (ascii_lowercase if lower else "") + (ascii_uppercase if upper else "") + (digits if num else "")
    random = _random_ins.setdefault(seed, Random(seed))
    if generate_num == 1:
        return _gen_str(random.choice, s, length)
    else:
        return [_gen_str(random.choice, s, length) for _ in range(generate_num)]


def _is_pos_far_enough(poses, x, y, z, min_distance):
    for pos in poses:
        if pos_distance(pos, (x, y, z)) < min_distance:
            return False
    return True


def random_even_poses(center_pos, radius, pos_num, fixed_x=False, fixed_y=False, fixed_z=False, min_distance=1.0):
    """
    | 在指定坐标周围，生成随机的均匀分布的多个坐标。
    
    -----

    :param tuple[float,float,float] center_pos: 中心坐标
    :param float radius: 生成半径
    :param int pos_num: 生成的坐标数量
    :param bool fixed_x: 是否固定x轴，固定后x轴取值将总是与center_pos一致，默认为不固定
    :param bool fixed_y: 是否固定y轴，固定后y轴取值将总是与center_pos一致，默认为不固定
    :param bool fixed_z: 是否固定z轴，固定后z轴取值将总是与center_pos一致，默认为不固定
    :param float min_distance: 生成的坐标之间的最小距离，越小生成的坐标越不均匀，默认为1.0

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    poses = []
    while len(poses) < pos_num:
        theta = uniform(0, 2 * pi)
        phi = uniform(0, pi)
        r = uniform(0, radius)
        x = center_pos[0] if fixed_x else center_pos[0] + r * sin(phi) * cos(theta)
        y = center_pos[1] if fixed_y else center_pos[1] + r * sin(phi) * sin(theta)
        z = center_pos[2] if fixed_z else center_pos[2] + r * cos(phi)
        if not poses or _is_pos_far_enough(poses, x, y, z, min_distance):
            poses.append((x, y, z))
    return poses


if __name__ == "__main__":
    print(random_string(20, lower=False))
    print(random_string(20, upper=False))
    print(random_string(20, num=False))
    print(random_string(20, num=False, seed=20230315, generate_num=5))
    for i in range(5):
        print(random_string(20, num=False, seed=20230315))

























