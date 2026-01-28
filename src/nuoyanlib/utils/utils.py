# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-19
#  ⠀
# =================================================


import traceback
from functools import wraps
import time
import re
from ..core._sys import get_lv_comp, is_client
from ..core._utils import singleton, lru_cache, cached_property, try_exec, iter_obj_attrs


if 0:
    from typing import Any


__all__ = [
    "rgb2hex",
    "hex2rgb",
    "get_time",
    "timeit",
    "notify_error",
    "call_interval",
    "check_string",
    "convert_dict_value_to_tuple",
    "convert_list_to_tuple",
    "translate_time",
    "singleton",
    "lru_cache",
    "cached_property",
    "try_exec",
    "iter_obj_attrs",
]


def rgb2hex(rgb_color, mc_rgb=True, with_sign=True, upper=True):
    """
    将 RGB 元组转换为 16 进制颜色代码 ``#RRGGBB`` 。

    -----

    :param tuple[float,float,float]|tuple[int,int,int] rgb_color: RGB 元组
    :param bool mc_rgb: 是否是 Minecraft RGB（取值范围为 0-1）；默认为 True
    :param bool with_sign: 返回的 16 进制颜色代码是否包含 "#" 前缀；默认为 True
    :param bool upper: 返回的 16 进制颜色代码是否大写；默认为 True

    :return: 16 进制颜色代码
    :rtype: str

    :raise ValueError: rgb_color 格式有误时抛出
    """
    if len(rgb_color) != 3:
        raise ValueError("rgb color must be of 3 elements.")

    if mc_rgb and all(0 <= c <= 1 for c in rgb_color):
        rgb_color = tuple(int(c * 255) for c in rgb_color)
    elif not mc_rgb and all(isinstance(c, int) and 0 <= c <= 255 for c in rgb_color):
        pass
    else:
        raise ValueError("illegal rgb color: " + repr(rgb_color))

    hex_color = "%02x%02x%02x" % rgb_color
    if upper:
        hex_color = hex_color.upper()
    if with_sign:
        hex_color = "#" + hex_color
    return hex_color


def hex2rgb(hex_color, mc_rgb=True):
    """
    将 16 进制颜色代码 ``#RRGGBB`` 转换为 RGB 元组。

    -----

    :param str hex_color: 16 进制颜色代码，可不包含 "#" 前缀
    :param bool mc_rgb: 是否转换为 Minecraft RGB 格式（取值范围为 0-1）；默认为 True

    :return: RGB 元组
    :rtype: tuple[float,float,float]|tuple[int,int,int]

    :raise ValueError: hex_color 格式有误时抛出
    """
    if hex_color[0] == "#":
        hex_color = hex_color[1:]
    if len(hex_color) != 6:
        raise ValueError("hex color must be 6 characters long (excluding '#')")

    r_hex = hex_color[0:2]
    g_hex = hex_color[2:4]
    b_hex = hex_color[4:6]
    r = int(r_hex, 16)
    g = int(g_hex, 16)
    b = int(b_hex, 16)
    if mc_rgb:
        r /= 255.0
        g /= 255.0
        b /= 255.0
    return r, g, b


def get_time():
    """
    获取当前时间。

    说明
    ----

    仅用于计时，PC 端返回 ``time.clock()`` （精度更高，非真实时间），移动端返回 ``time.time()`` 。

    -----

    :return: 当前时间
    :rtype: float
    """
try:
    get_time = time.clock
except AttributeError:
    try:
        get_time = time.perf_counter
    except AttributeError:
        get_time = time.time


def timeit(func, n=100000, print_res=False, args=None, kwargs=None):
    """
    计算函数执行耗时。

    -----

    :param function func: 函数
    :param int n: 执行次数；默认为 100000
    :param bool print_res: 是否打印计算结果；默认为 False
    :param Any args: 函数位置参数元组；默认为 None
    :param Any kwargs: 函数关键字参数字典；默认为 None

    :return: 返回一个元组：(总耗时, 平均耗时)，单位为毫秒
    :rtype: tuple[float,float]
    """
    args = args or ()
    kwargs = kwargs or {}
    t = get_time()
    for _ in xrange(n):
        func(*args, **kwargs)
    total = get_time() - t
    total *= 1000
    avg = total / n
    if print_res:
        print(
            "[timeit] func: {}(), total: {:.3f}ms, average: {:.3f}ms, n: {}"
            .format(func.__name__, total, avg, n)
        )
    return total, avg


def notify_error(player_id=None):
    """
    将最近一次的报错信息打印到聊天栏。

    -----

    :param str|None player_id: 打印到的玩家实体ID，客户端调用时可省略该参数

    :return: 无
    :rtype: None
    """
    client = is_client()
    lv_comp = get_lv_comp()
    for line in traceback.format_exc().splitlines():
        if client:
            lv_comp.TextNotifyClient.SetLeftCornerNotify(line)
        else:
            lv_comp.Msg.NotifyOneMessage(player_id, line)


def call_interval(interval):
    """
    [装饰器]

    限制函数调用的最小时间间隔。

    -----

    :param float interval: 最小时间间隔，单位为秒
    """
    def decorator(func):
        func._nyl__last_call_time = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - func._nyl__last_call_time >= interval:
                func._nyl__last_call_time = now
                return func(*args, **kwargs)

        return wrapper
    return decorator


def check_string(string, *check):
    """
    检测字符串是否 **只含有** 指定字符。
    
    -----

    :param str string: 字符串
    :param str check: [变长位置参数] 检测元素，可用 "0-9" 表示所有数字，"a-z" 表示所有小写字母，"A-Z" 表示所有大写字母

    :return: 是否只含有指定字符
    :rtype: bool
    """
    for i in string:
        if "a-z" in check and re.match("[a-z]", i):
            continue
        if "A-Z" in check and re.match("[A-Z]", i):
            continue
        if "0-9" in check and re.match("[0-9]", i):
            continue
        if i in check:
            continue
        return False
    return True


def convert_dict_value_to_tuple(dct):
    """
    将字典值中的所有列表递归转换为元组（直接修改字典）。
    
    -----

    :param dict dct: 字典

    :return: 原字典
    :rtype: dict
    """
    for key, value in dct.items():
        if isinstance(value, list):
            dct[key] = convert_list_to_tuple(value)
    return dct


def convert_list_to_tuple(lst):
    """
    将列表及其元素中的列表转换成元组（递归转换）。
    
    -----

    :param list lst: 列表

    :return: 转换后的元组
    :rtype: tuple
    """
    new_lst = []
    for i in lst:
        if isinstance(i, list):
            new_lst.append(convert_list_to_tuple(i))
        else:
            new_lst.append(i)
    return tuple(new_lst)


def translate_time(sec, separator="", unit=("h", "m", "s"), zfill=False):
    """
    将秒数转换成 h/m/s 的格式字符串。

    -----

    :param int sec: 秒数
    :param str separator: 分隔符；默认为空字符串
    :param tuple[str,str,str] unit: 时间单位，三元组，对应时分秒，传入 None 则表示不带单位；默认为 ("h", "m", "s")
    :param bool zfill: 是否在数字前补零；默认为 False

    :return: h/m/s 格式字符串
    :rtype: str
    """
    sec = int(sec)
    if unit is None:
        unit = ("", "", "")
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    parts = []
    hs = ms = ss = ""
    if h:
        hs = str(h) + unit[0]
        parts.append(hs)
    if m or zfill:
        ms = str(m)
        if zfill and hs:
            ms = ms.zfill(2)
        ms += unit[1]
        parts.append(ms)
    if s or zfill or (not hs and not ms):
        ss = str(s)
        if zfill and (hs or ms):
            ss = ss.zfill(2)
        ss += unit[2]
        parts.append(ss)
    return separator.join(parts)


def __test__():
    from ..core._utils import assert_error

    assert rgb2hex((255, 69, 0), False) == "#FF4500"
    assert rgb2hex((255, 69, 0), False, False, False) == "ff4500"
    assert rgb2hex((0, 0, 0)) == "#000000"
    assert_error(rgb2hex, ((255, 69), False), exc=ValueError)
    assert_error(rgb2hex, ((255, 69, 300), False), exc=ValueError)

    assert hex2rgb("#FF4500", False) == (255, 69, 0)
    assert hex2rgb("#000000", True) == (0, 0, 0)
    assert_error(hex2rgb, ("#FF45",), exc=ValueError)
    assert_error(hex2rgb, ("#FF45AV",), exc=ValueError)

    assert check_string("11112222", "1", "2")
    assert not check_string("11112222", "1")
    assert check_string("1234567890", "0-9")

    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    convert_dict_value_to_tuple(a)
    assert a == {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}

    a = [1, [2, 3], "abc"]
    assert convert_list_to_tuple(a) == (1, (2, 3), "abc")

    assert translate_time(3660, ":", ("H", "M", "S"), True) == "1H:01M:00S"
    assert translate_time(3660, unit=("H", "M", "S"), zfill=True) == "1H01M00S"
    assert translate_time(3660, unit=("H", "M", "S"), zfill=False) == "1H1M"
    assert translate_time(3661, ":", None, True) == "1:01:01"
    assert translate_time(3660, ":", None, True) == "1:01:00"
    assert translate_time(3600, ":", None, True) == "1:00:00"
    assert translate_time(61, ":", None, True) == "1:01"
    assert translate_time(60, ":", None, True) == "1:00"
    assert translate_time(1, ":", None, True) == "0:01"
    assert translate_time(0, ":", None, True) == "0:00"
    assert translate_time(3700) == "1h1m40s"
    assert translate_time(3660) == "1h1m"
    assert translate_time(3601) == "1h1s"
    assert translate_time(61) == "1m1s"
    assert translate_time(3600) == "1h"
    assert translate_time(60) == "1m"
    assert translate_time(1) == "1s"
    assert translate_time(0) == "0s"




















