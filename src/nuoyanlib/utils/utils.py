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
    from typing import Any, Sequence


from functools import wraps
import time
import re
from ..core._sys import get_lib_system, get_lv_comp, is_client
from ..core._utils import singleton, lru_cache, cached_property


__all__ = [
    "rgb_to_hex",
    "hex_to_rgb",
    "get_time",
    "timeit",
    "notify_error",
    "call_interval",
    "add_condition_to_func",
    "rm_condition_to_func",
    "all_indexes",
    "check_string",
    "check_string2",
    "turn_dict_value_to_tuple",
    "turn_list_to_tuple",
    "is_method_overridden",
    "translate_time",
    "singleton",
    "lru_cache",
    "cached_property",
]


def rgb_to_hex(rgb_color, with_sign=True, upper=True):
    """
    将 ``(R,⠀G,⠀B)`` 元组转换为 16 进制颜色代码 ``#RRGGBB`` 。

    -----

    :param tuple[float,float,float]|tuple[int,int,int] rgb_color: RGB 元组，支持 Minecraft RGB 格式（取值范围为 0-1）
    :param bool with_sign: 返回的 16 进制颜色代码是否包含 "#" 前缀；默认为 True
    :param bool upper: 返回的 16 进制颜色代码是否大写；默认为 True

    :return: 16 进制颜色代码
    :rtype: str

    :raise ValueError: RGB 元组格式有误时抛出
    """
    if len(rgb_color) != 3:
        raise ValueError("'rgb_color' must be of 3 elements.")

    if all(0 <= c <= 1 for c in rgb_color):
        rgb_color = tuple(int(c * 255) for c in rgb_color)
    elif all(isinstance(c, int) and 0 <= c <= 255 for c in rgb_color):
        pass
    else:
        raise ValueError("illegal rgb color: %s" % str(rgb_color))

    hex_color = "%02x%02x%02x" % rgb_color
    if upper:
        hex_color = hex_color.upper()
    if with_sign:
        hex_color = "#" + hex_color
    return hex_color


def hex_to_rgb(hex_color, mc_rgb=True):
    """
    将 16 进制颜色代码 ``#RRGGBB`` 转换为 ``(R,⠀G,⠀B)`` 元组。

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
        raise ValueError("'hex_color' must be 6 characters long")

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

    :return: 返回一个元组，元素分别为总耗时和平均耗时，单位为 ms
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
    将报错信息打印到聊天栏。

    -----

    :param str|None player_id: 打印到的玩家实体ID，客户端可省略该参数

    :return: 无
    :rtype: None
    """
    from traceback import format_exc
    client = is_client()
    lv_comp = get_lv_comp()
    for line in format_exc().splitlines():
        if client:
            lv_comp.TextNotifyClient.SetLeftCornerNotify(line)
        else:
            lv_comp.Msg.NotifyOneMessage(player_id, line)


def call_interval(interval):
    """
    [装饰器]

    用于限制函数调用的最小时间间隔。

    -----

    :param float interval: 最小时间间隔，单位为秒
    """
    def decorator(func):
        func._last_call_time = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - func._last_call_time >= interval:
                func._last_call_time = now
                return func(*args, **kwargs)
        return wrapper
    return decorator


def add_condition_to_func(cond, func, freq=1):
    """
    为指定函数添加一个条件，当条件发生变化时，自动执行一次函数。

    例如，当条件由 ``True`` 变化到 ``False``，或由 ``False`` 变化到 ``True`` 时，都会执行一次指定函数。

    -----

    :param function cond: 条件函数，无参数，需要返回一个 bool，当返回的 bool（即条件）发生变化时，自动执行一次 func
    :param function func: 条件发生变化时执行的函数，该函数需要接受一个类型为 bool 的参数，即当前的条件状态（cond 的返回值）
    :param int freq: 条件判断频率，单位为 tick；默认为 1，即每 tick 判断一次，小于 1 的值会被视为 1

    :return: 返回一个 int 型ID，后续可用该ID移除添加的条件和函数，添加失败时返回 -1
    :rtype: int
    """
    freq = max(1, int(freq))
    lib_sys = get_lib_system()
    if not lib_sys:
        return -1
    return lib_sys.add_condition_to_func(cond, func, freq)


def rm_condition_to_func(cond_id):
    """
    移除由 ``add_condition_to_func()`` 添加的条件和函数。

    -----

    :param int cond_id: 由 add_condition_to_func() 返回的ID

    :return: 是否成功
    :rtype: bool
    """
    lib_sys = get_lib_system()
    if not lib_sys:
        return False
    return lib_sys.rm_condition_to_func(cond_id)


def all_indexes(seq, *elements):
    """
    获取元素在序列中所有出现位置的下标。
    
    -----

    :param Sequence seq: 任意序列，可以是列表、元组、字符串等
    :param Any elements: 待查找元素

    :return: 元素所有出现位置的下标列表
    :rtype: list[int]
    """
    return [i for i, e in enumerate(seq) if e in elements]


def check_string(string, *check):
    """
    检测字符串是否只含有指定字符。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用 "0-9" 表示所有数字，"a-z" 表示所有小写字母，"A-Z" 表示所有大写字母

    :return: 只含有指定字符则返回 True, 否则返回 False
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


def check_string2(string, *check):
    """
    返回字符串中指定字符之外的字符的列表。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用 "0-9" 表示所有数字，"a-z" 表示所有小写字母，"A-Z" 表示所有大写字母

    :return: 指定字符之外的字符的列表
    :rtype: list[str]
    """
    result = []
    for i in string:
        if i in check:
            continue
        if "a-z" in check and re.match("[a-z]", i):
            continue
        if "A-Z" in check and re.match("[A-Z]", i):
            continue
        if "0-9" in check and re.match("[0-9]", i):
            continue
        result.append(i)
    return result


def turn_dict_value_to_tuple(org_dict):
    """
    将字典值中的列表全部转换为元组。（改变原字典）
    
    -----

    :param dict org_dict: 字典

    :return: 无
    :rtype: None
    """
    for key, value in org_dict.items():
        if isinstance(value, list):
            org_dict[key] = turn_list_to_tuple(value)


def turn_list_to_tuple(lst):
    """
    将一个列表及其元素中的列表转换成元组。
    
    -----

    :param list lst: 列表

    :return: 转换后的元组
    :rtype: tuple
    """
    new_lst = []
    for i in lst:
        if isinstance(i, list):
            new_lst.append(turn_list_to_tuple(i))
        else:
            new_lst.append(i)
    return tuple(new_lst)


def is_method_overridden(subclass, father, method):
    """
    判断子类是否重写了父类的方法。
    
    -----

    :param Any subclass: 子类
    :param Any father: 父类
    :param str method: 方法名

    :return: 方法被重写返回 True，否则返回 False
    :rtype: bool
    """
    subclass_method = getattr(subclass, method)
    father_method = getattr(father, method)
    return subclass_method != father_method


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
    assert rgb_to_hex((255, 69, 0)) == "#FF4500"
    assert rgb_to_hex((255, 69, 0), with_sign=False, upper=False) == "ff4500"
    assert rgb_to_hex((0, 0, 0)) == "#000000"
    assert_error(rgb_to_hex, ((255, 69),), exc=ValueError)
    assert_error(rgb_to_hex, ((255, 69, 300),), exc=ValueError)

    assert hex_to_rgb("#FF4500", False) == (255, 69, 0)
    assert hex_to_rgb("#000000", True) == (0, 0, 0)
    assert_error(hex_to_rgb, ("#FF45",), exc=ValueError)
    assert_error(hex_to_rgb, ("#FF45AV",), exc=ValueError)

    assert all_indexes([1, 1, 4, 5, 1, 4], 1) == [0, 1, 4]
    assert all_indexes([1, 1, 4, 5, 1, 4], 1, 4) == [0, 1, 2, 4, 5]
    assert all_indexes("abcdefg", "c", "g") == [2, 6]
    assert check_string("11112222", "1", "2")
    assert not check_string("11112222", "1")
    assert check_string("1234567890", "0-9")
    assert check_string2("abc123", "a", "c", "3") == ["b", "1", "2"]
    assert check_string2("abc123", "a-z") == ["1", "2", "3"]
    assert check_string2("abc123", "0-9") == ["a", "b", "c"]

    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    turn_dict_value_to_tuple(a)
    assert a == {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}

    a = [1, [2, 3], "abc"]
    assert turn_list_to_tuple(a) == (1, (2, 3), "abc")

    class A:
        def printIn(self, s):
            print(s)
    class B(A):
        def printIn(self, s):
            print(1)
    class C(A):
        pass
    assert is_method_overridden(B, A, "printIn")
    assert not is_method_overridden(C, A, "printIn")

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




















