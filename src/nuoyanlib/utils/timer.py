# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-11
|
| ====================================================
"""


import threading
from ..core._sys import get_lv_comp, is_client


__all__ = [
    "delay",
    "repeat",
    # "Timer",
]


_c_delay_timers = {}
_s_delay_timers = {}
_c_repeat_timers = {}
_s_repeat_timers = {}


def _set_timer(t, func, is_repeat, key):
    if is_client():
        if is_repeat:
            dct = _c_repeat_timers
        else:
            dct = _c_delay_timers
    else:
        if is_repeat:
            dct = _s_repeat_timers
        else:
            dct = _s_delay_timers
    comp = get_lv_comp().Game
    if key is not None and key in dct:
        comp.CancelTimer(dct[key])
    if is_repeat:
        dct[key] = comp.AddRepeatedTimer(t, func)
    else:
        def timeout():
            dct.pop(key, None)
            func()
        dct[key] = comp.AddTimer(t, timeout)


def delay(t=0, key=None):
    """
    [装饰器]

    定时器，延迟指定时间执行函数（仅支持无参数的函数）。

    -----

    :param float t: 延迟时间，单位秒；默认为0，表示下一帧执行
    :param Any key: 定时器键名，用于标识定时器，可传入str、int、tuple等可哈希对象；传入该参数时，若存在相同键名且尚未触发的定时器，则旧的定时器会被取消；默认为None
    """
    def decorator(func):
        _set_timer(_t, func, False, key)
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

    :param float t: 执行间隔时间，单位秒；默认为0，表示每帧执行
    :param Any key: 定时器键名，用于标识定时器，可传入str、int、tuple等可哈希对象；传入该参数时，若存在相同键名的定时器，则旧的定时器会被取消；默认为None
    """
    def decorator(func):
        _set_timer(_t, func, True, key)
        return func
    if callable(t):
        _t = 0
        return decorator(t)
    else:
        _t = t
        return decorator


class Timer(object):
    """
    客户端函数定时器。

    非重复执行的定时器在执行完毕后会自动销毁。
    与官方的定时器不同的是，该定时器使用threading标准库实现，比官方的定时器计时更精准。

    -----

    :param str ttype: 定时器类型，可选值为"d"和"r"，分别表示普通定时器和重复定时器
    :param float sec: 延迟秒数
    :param function func: 延迟函数
    :param Any args: [变长位置参数] 调用func时传入
    :param Any kwargs: [变长关键字参数] 调用func时传入
    """

    def __init__(self, ttype, sec, func, *args, **kwargs):
        self.type = ttype
        self.sec = sec
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._pause = False
        self._cancel = False
        self.__timer = threading.Timer(sec, self.__func)

    def _execute(self):
        return self.func(*self.args, **self.kwargs)

    def __func(self):
        self._execute()
        if self.type == "r" and not self._cancel:
            self.__timer = threading.Timer(self.sec, self.__func)
            self.__timer.start()
        else:
            self._release()

    def Start(self):
        """
        启动定时器。

        -----

        :return: 定时器自身
        :rtype: Timer
        """
        self.__timer.start()
        return self

    def Cancel(self):
        """
        取消定时器。

        -----

        :return: 无
        :rtype: None
        """
        self.__timer.cancel()
        self._release()

    def _release(self):
        self.__timer = None
        self._cancel = True
        self._pause = False
        self.sec = -1
        self.func = None
        self.args = None
        self.kwargs = None

    def Pause(self, sec=None):
        # todo: Pause
        """
        暂停定时器，重复调用时仅第一次有效。

        -----

        :param float|None sec: 暂停秒数，默认为None，表示无限期暂停

        :return: 定时器自身
        :rtype: Timer
        """
        if not self._pause:
            pass
        return self

    def Continue(self):
        # todo: Continue
        """
        继续运行被暂停的定时器。

        -----

        :return: 定时器自身
        :rtype: Timer
        """
        if self._pause:
            pass
        return self

    def Execute(self):
        """
        立即执行一次函数。

        -----

        :return: 返回原函数的返回值
        :rtype: Any
        """
        return self._execute()

    def IsCanceled(self):
        """
        获取定时器是否已经取消。

        -----

        :return: 定时器正在运行时返回True，定时器已取消或执行完毕时返回False
        :rtype: bool
        """
        return self._cancel

    def IsPaused(self):
        """
        获取定时器是否暂停。

        -----

        :return: 是否暂停
        :rtype: bool
        """
        return not self._cancel and self._pause


if __name__ == "__main__":
    def func1(x, y):
        print(x + y)
    timer1 = Timer("d", 1, func1, 1, 2)
    a = []
    def func2(x):
        a.append(x)
        print(a)
        if len(a) >= 3:
            timer2.Cancel()
    timer2 = Timer("r", 2, func2, 1)
    timer1.Start()
    timer2.Start()
    def func3():
        print(114514)
    timer3 = Timer("d", 2, func3).Start()
    def func4():
        timer3.Cancel()
        print("stop 114514")
    Timer("d", 1, func4).Start()














