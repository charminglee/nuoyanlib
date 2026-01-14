# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


if 0:
    from typing import Any


import random
import string
from ..core._sys import get_lv_comp
from ..core._utils import inject_is_client, UNIVERSAL_OBJECT
from .mc_math import pos_floor


__all__ = [
    "chance",
    "random_pos",
    "random_string",
]


if 0:
    # 绕过机审专用
    random_pos = lambda *_, **__: UNIVERSAL_OBJECT


def chance(p):
    """
    以指定概率返回 ``True`` 。

    -----

    :param float p: 概率，范围为 [0, 1]

    :return: 以 p 的概率返回 True，否则返回 False
    :rtype: bool
    """
    return p > random.random()


@inject_is_client
def random_pos(__is_client__, center, r, dim=None, use_top_height=False):
    """
    在指定区域内随机获取一点坐标。
    
    -----

    :param tuple[float,float,float] center: 区域中心坐标
    :param float r: 区域半径
    :param int|None dim: 维度ID，若在客户端调用可忽略该参数；默认为 None
    :param bool use_top_height: 是否以最高的非空气方块的高度作为返回坐标的y值；默认为 False

    :return: 坐标，获取失败时返回 None
    :rtype: tuple[float,float,float]|None
    """
    if not center:
        return
    x = center[0] + random.uniform(-r, r)
    z = center[2] + random.uniform(-r, r)
    if use_top_height:
        pos = pos_floor((x, z))
        if __is_client__:
            y = get_lv_comp().BlockInfo.GetTopBlockHeight(pos)
        else:
            if dim is None:
                dim = 0
            y = get_lv_comp().BlockInfo.GetTopBlockHeight(pos, dim)
        if y is not None:
            return x, y, z
    else:
        y = center[1] + random.uniform(-r, r)
        return x, y, z


def _gen_str(choice, s, l):
    return "".join(choice(s) for _ in xrange(l))


_random_ins = {}


def random_string(length, lower=True, upper=True, num=True, seed=None, generate_num=1):
    """
    生成随机字符串。
    
    -----

    :param int length: 生成的字符串长度
    :param bool lower: 是否包含小写字母；默认为 True
    :param bool upper: 是否包含大写字母；默认为 True
    :param bool num: 是否包含数字；默认为 True
    :param Any|None seed: 随机数种子；默认为 None
    :param int generate_num: 生成数量；默认为 1，大于 1 时将以列表返回结果

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

    if seed not in _random_ins:
        _random_ins[seed] = random.Random(seed)
    rand = _random_ins[seed]

    if generate_num == 1:
        return _gen_str(rand.choice, s, length)
    else:
        return [_gen_str(rand.choice, s, length) for _ in xrange(generate_num)]


def __test__():
    return
    print(random_string(20, lower=False))
    print(random_string(20, upper=False))
    print(random_string(20, num=False))
    print(random_string(20, num=False, seed=20230315, generate_num=5))
    for i in range(5):
        print(random_string(20, num=False, seed=20230315))

























