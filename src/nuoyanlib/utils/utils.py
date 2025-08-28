# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-23
|
| ==============================================
"""


from functools import wraps
from time import time
from re import match
from .._core._sys import get_lib_system


__all__ = [
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
]


def call_interval(interval):
    """
    [装饰器]

    | 用于限制函数调用的最小时间间隔。

    -----

    :param float interval: 最小时间间隔，单位为秒

    :return: 返回wrapper函数
    :rtype: function
    """
    def decorator(func):
        func._last_call_time = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            if now - func._last_call_time >= interval:
                func._last_call_time = now
                return func(*args, **kwargs)
        return wrapper
    return decorator


def add_condition_to_func(cond, func, freq=1):
    """
    | 为指定函数添加一个条件，当条件发生变化时，自动执行一次函数。例如，当条件由 ``True`` 变化到 ``False``，或由 ``False`` 变化到 ``True`` 时，都会执行一次指定函数。

    -----

    :param function cond: 条件函数，无参数，需要返回一个bool，当返回的bool（即条件）发生变化时，自动执行一次func
    :param function func: 条件发生变化时执行的函数，该函数需要接受一个类型为bool的参数，即当前的条件状态（cond的返回值）
    :param int freq: 条件判断频率，单位为tick，默认为1，即每1tick判断一次，小于1的值会被视为1

    :return: 返回一个int型ID，后续可用该ID移除添加的条件和函数，添加失败时返回-1
    :rtype: int
    """
    freq = max(1, int(freq))
    lib_sys = get_lib_system()
    if not lib_sys:
        return -1
    return lib_sys.add_condition_to_func(cond, func, freq)


def rm_condition_to_func(cond_id):
    """
    | 移除由 ``add_condition_to_func()`` 添加的条件和函数。

    -----

    :param int cond_id: 由add_condition_to_func返回的ID

    :return: 是否成功
    :rtype: bool
    """
    lib_sys = get_lib_system()
    if not lib_sys:
        return False
    return lib_sys.rm_condition_to_func(cond_id)


def all_indexes(seq, *elements):
    """
    | 获取元素在序列中所有出现位置的下标。
    
    -----

    :param Sequence seq: 任意序列，可以是列表、元组、字符串等
    :param Any elements: 待查找元素

    :return: 元素所有出现位置的下标列表
    :rtype: list[int]
    """
    return [i for i, e in enumerate(seq) if e in elements]


def check_string(string, *check):
    """
    | 检测字符串是否只含有指定字符。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母

    :return: 只含有指定字符则返回True, 否则返回False
    :rtype: bool
    """
    for i in string:
        if "a-z" in check and match("[a-z]", i):
            continue
        if "A-Z" in check and match("[A-Z]", i):
            continue
        if "0-9" in check and match("[0-9]", i):
            continue
        if i in check:
            continue
        return False
    return True


def check_string2(string, *check):
    """
    | 返回字符串中指定字符之外的字符的列表。
    
    -----

    :param str string: 字符串
    :param str check: 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母

    :return: 指定字符之外的字符的列表
    :rtype: list[str]
    """
    result = []
    for i in string:
        if i in check:
            continue
        if "a-z" in check and match("[a-z]", i):
            continue
        if "A-Z" in check and match("[A-Z]", i):
            continue
        if "0-9" in check and match("[0-9]", i):
            continue
        result.append(i)
    return result


def turn_dict_value_to_tuple(orig_dict):
    """
    | 将字典值中的列表全部转换为元组。（改变原字典）
    
    -----

    :param dict orig_dict: 字典

    :return: 无
    :rtype: None
    """
    for key, value in orig_dict.items():
        if isinstance(value, list):
            orig_dict[key] = turn_list_to_tuple(value)


def turn_list_to_tuple(lst):
    """
    | 将一个列表及其元素中的列表转换成元组。
    
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
    | 判断子类是否重写了父类的方法。
    
    -----

    :param Any subclass: 子类
    :param Any father: 父类
    :param str method: 方法名

    :return: 方法被重写返回True，否则返回False
    :rtype: bool
    """
    subclass_method = getattr(subclass, method)
    father_method = getattr(father, method)
    return subclass_method != father_method


def translate_time(sec, separator="", unit=("h", "m", "s"), zfill=False):
    """
    | 将秒数转换成h/m/s的格式字符串。

    -----

    :param int sec: 秒数
    :param str separator: 分隔符，默认为空字符串
    :param tuple[str,str,str] unit: 时间单位，三元组，对应时分秒，传入None则表示不带单位；默认为("h", "m", "s")
    :param bool zfill: 是否在数字前补零，默认为False

    :return: h/m/s格式字符串
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


if __name__ == "__main__":
    __test__()




















