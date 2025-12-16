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


if 0:
    from typing import Any


import math
import random
import string
from ..core._sys import get_lv_comp, is_client


__all__ = [
    "random_pos",
    "random_string",
    "random_even_poses",
]


def random_pos(center_pos, r, dim=0, use_top_height=False):
    """
    在指定区域内随机获取一点坐标。
    
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
    x = center_pos[0] + random.uniform(-r, r)
    z = center_pos[2] + random.uniform(-r, r)
    if use_top_height:
        if is_client():
            y = get_lv_comp(True).BlockInfo.GetTopBlockHeight((x, z))
        else:
            y = get_lv_comp(False).BlockInfo.GetTopBlockHeight((x, z), dim)
        if y is not None:
            return x, y, z
    else:
        y = center_pos[1] + random.uniform(-r, r)
        return x, y, z


def _gen_str(choice, s, l):
    return "".join(choice(s) for _ in range(l))


_random_ins = {}


def random_string(length, lower=True, upper=True, num=True, seed=None, generate_num=1):
    """
    生成随机字符串。
    
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
    s = ""
    if lower:
        s += string.ascii_lowercase
    if upper:
        s += string.ascii_uppercase
    if num:
        s += string.digits
    rand = _random_ins.setdefault(seed, random.Random(seed))
    if generate_num == 1:
        return _gen_str(rand.choice, s, length)
    else:
        return [_gen_str(rand.choice, s, length) for _ in range(generate_num)]


def random_even_poses(center_pos, radius, pos_num, fixed_x=False, fixed_y=False, fixed_z=False):
    """
    在指定坐标周围，生成随机的均匀分布的多个坐标。
    
    -----

    :param tuple[float,float,float] center_pos: 中心坐标
    :param float radius: 生成半径
    :param int pos_num: 生成的坐标数量
    :param bool fixed_x: 是否固定x轴，固定后x轴取值将总是与center_pos一致，默认为不固定
    :param bool fixed_y: 是否固定y轴，固定后y轴取值将总是与center_pos一致，默认为不固定
    :param bool fixed_z: 是否固定z轴，固定后z轴取值将总是与center_pos一致，默认为不固定

    :return: 坐标列表
    :rtype: list[tuple[float,float,float]]
    """
    cx, cy, cz = center_pos
    poses = []
    for _ in range(pos_num):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = radius * (random.random() ** (1/3.))
        pos = (
            cx if fixed_x else cx + r * math.sin(phi) * math.cos(theta),
            cy if fixed_y else cy + r * math.sin(phi) * math.sin(theta),
            cz if fixed_z else cz + r * math.cos(phi),
        )
        poses.append(pos)
    return poses


if __name__ == "__main__":
    print(random_string(20, lower=False))
    print(random_string(20, upper=False))
    print(random_string(20, num=False))
    print(random_string(20, num=False, seed=20230315, generate_num=5))
    for i in range(5):
        print(random_string(20, num=False, seed=20230315))

























