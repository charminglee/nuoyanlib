# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-16
#  ⠀
# =================================================


from ..core._sys import get_lv_comp
from ..core._utils import DefaultLocal


if 0:
    from typing import Any


__all__ = [
    "delay",
    "repeat",
]


_timers = DefaultLocal(dict)


def _add_timer(t, func, is_repeat, key):
    timer_dct = _timers.repeat if is_repeat else _timers.delay
    comp = get_lv_comp().Game
    if key is not None and key in timer_dct:
        comp.CancelTimer(timer_dct[key])
    if is_repeat:
        timer_dct[key] = comp.AddRepeatedTimer(t, func)
    else:
        def timeout():
            timer_dct.pop(key, None)
            func()
        timer_dct[key] = comp.AddTimer(t, timeout)


def delay(t=0, key=None):
    """
    [装饰器]

    定时器，延迟指定时间执行函数（仅支持无参数的函数）。

    -----

    :param float t: 延迟时间，单位秒；默认为 0，表示下一帧执行
    :param Any key: 定时器键名，用于标识定时器，可传入 str、int、tuple 等可哈希对象；传入该参数时，若存在相同键名且尚未触发的定时器，则旧的定时器会被取消；默认为 None
    """
    def decorator(func):
        _add_timer(_t, func, False, key)
        return func
    if callable(t):
        _t = 0
        return decorator(t)
    else:
        _t = t
        return decorator


def repeat(t=0, key=None):
    """
    [装饰器]

    定时器，以指定时间间隔重复执行函数（仅支持无参数的函数）。

    -----

    :param float t: 执行间隔时间，单位秒；默认为 0，表示每帧执行
    :param Any key: 定时器键名，用于标识定时器，可传入 str、int、tuple 等可哈希对象；传入该参数时，若存在相同键名的定时器，则旧的定时器会被取消；默认为 None
    """
    def decorator(func):
        _add_timer(_t, func, True, key)
        return func
    if callable(t):
        _t = 0
        return decorator(t)
    else:
        _t = t
        return decorator
















