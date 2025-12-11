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


import time
from .enum import TimeEaseFunc


__all__ = [
    "TimeEase",
]


class TimeEase(object):
    """
    时间缓动类。

    内置各种时间缓动函数，可用于实现UI动画、运镜等的平滑过渡效果。

    时间缓动对象为一个迭代器，每次迭代或调用 ``.next()`` 方法时，会返回最新的缓动值。缓动值按照以下公式进行计算：

    ::

        start_val⠀+⠀ease_func(x)⠀*⠀(end_val⠀-⠀start_val)

    其中，参数 ``x`` 表示经过的时间比例，取值范围为 [0, 1]。

    -----

    :param float start_val: 初始值
    :param float end_val: 最终值
    :param float total_tm: 变化总时间，单位为秒
    :param int fps: 变化帧率，小于等于0的值将根据真实时间确定缓动值，默认为0
    :param bool hold_on_last_frame: 是否停止在最后一帧；若设为True，TimeEase可无限迭代，变化结束后将始终返回最后一帧的值；若设为False，变化结束后继续迭代将抛出StopIteration异常；默认为False
    :param function ease_func: 时间缓动函数，可使用TimeEaseFunc提供的函数或自定义函数，如线性函数 lambda x: x ，参数x表示经过的时间比例，取值范围为 [0,⠀1] ，即只取缓动函数定义域中 [0,⠀1] 部分的值；默认为TimeEaseFunc.linear
    :param TimeEase|None next_te: 下一个时间缓动对象，若提供，则当前缓动迭代结束后自动切换到下一个缓动对象继续迭代；默认为None
    :param function|None on_start: 缓动开始时调用的函数，默认为None
    :param function|None on_end: 缓动结束时调用的函数，默认为None

    :raise ValueError: 传入的参数错误，请检查参数是否符合要求
    """

    def __init__(
            self,
            start_val,
            end_val,
            total_tm,
            fps=0,
            hold_on_last_frame=False,
            ease_func=TimeEaseFunc.LINEAR,
            next_te=None,
            on_start=None,
            on_end=None,
    ):
        self.start_val = start_val
        self.end_val = end_val
        self.total_tm = total_tm
        self.fps = fps
        self.hold_on_last_frame = hold_on_last_frame
        self.ease_func = ease_func
        self.next_te = next_te
        self.on_start = on_start
        self.on_end = on_end
        self._init_tm = 0
        self._frame = 0
        self._total_frame = fps * total_tm
        self._diff_val = self.end_val - self.start_val
        self._val = 0
        self._state = 0

    def __iter__(self):
        return self

    def _on_start(self):
        self._state += 1
        if self.on_start:
            self.on_start()

    def _on_end(self):
        if self.on_end:
            self.on_end()
        self._state += 1
        if self.next_te:
            self.start_val = self.next_te.start_val
            self.end_val = self.next_te.end_val
            self.total_tm = self.next_te.total_tm
            self.fps = self.next_te.fps
            self.hold_on_last_frame = self.next_te.hold_on_last_frame
            self.ease_func = self.next_te.ease_func
            self.on_start = self.next_te.on_start
            self.on_end = self.next_te.on_end
            self.next_te = self.next_te.next_te
            self.reset()

    def next(self):
        """
        计算并返回下一个缓动值。

        -----

        :return: 下一个缓动值
        :rtype: None
        """
        if self._state == 0:
            self._on_start()
        elif self._state == 2:
            if self.hold_on_last_frame:
                return self._val
            else:
                raise StopIteration
        if self.total_tm <= 0:
            x = 1
        elif self.fps > 0:
            x = min(self._frame / self._total_frame, 1)
            self._frame += 1
        else:
            if self._init_tm == 0:
                self._init_tm = time.time()
            x = min((time.time() - self._init_tm) / self.total_tm, 1)
        self._val = self.start_val + self.ease_func(x) * self._diff_val
        if x >= 1:
            self._on_end()
        return self._val

    def reset(self):
        """
        重置状态，重头开始计算。

        -----

        :return: 无
        :rtype: None
        """
        self._init_tm = 0
        self._frame = 0
        self._total_frame = self.fps * self.total_tm
        self._diff_val = self.end_val - self.start_val
        self._state = 0

    def pause(self):
        pass
        # todo

















