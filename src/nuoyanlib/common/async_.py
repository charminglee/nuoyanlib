# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-3-25
#  ⠀
# =================================================


from functools import wraps
from .timer import _add_timer


__all__ = [
    "async_",
    "async_sleep",
]


def _next(gen):
    try:
        ret = next(gen)
    except StopIteration:
        return
    if isinstance(ret, async_sleep):
        _add_timer(ret.t, False, None, _next, gen)
    else:
        _next(gen)


def async_(func):
    """
    [装饰器]

    用于将函数定义为异步函数。

    可配合 ``nyl.async_sleep()`` 实现异步等待。

    示例
    ----

    执行以下函数后，将会每隔一秒打印一次计数，在此期间其他代码的执行不受影响。

    >>> @nyl.async_
    ... def count():
    ...     for i in range(10):
    ...         print(i)
    ...         yield nyl.async_sleep(1) # 等待1秒
    """
    if func.__code__.co_flags & 0x0020: # 判断传入的是否生成器函数 # noqa
        @wraps(func)
        def wrapper(*args, **kwargs):
            gen = func(*args, **kwargs)
            _next(gen)
        return wrapper
    else:
        return func


class async_sleep(object):
    """
    异步等待指定时间。

    只能在被 ``@nyl.async_`` 装饰的异步函数中使用。

    示例
    ----

    详见 ``@nyl.async_`` 。

    -----

    :param float t: 等待时间，单位秒
    """

    def __init__(self, t):
        self.t = t



















