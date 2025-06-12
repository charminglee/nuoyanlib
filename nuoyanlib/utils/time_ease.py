# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-06
|
| ==============================================
"""


from time import time
from math import pi, sin, cos, sqrt


__all__ = [
    "TimeEaseFunc",
    "TimeEase",
]


class TimeEaseFunc:
    """
    | 时间缓动函数枚举。
    """

    linear = staticmethod(lambda x: x)
    """
    | 线性缓动，变化速度均匀。
    """

    spring = staticmethod(lambda x: 1 - cos(x * pi * (0.2 + 2.5 * x**2)))
    """
    | 弹簧缓动，效果通常表现为一个有些反复的波动，随着时间逐渐衰减。
    """

    in_quad = staticmethod(lambda x: x**2)
    """
    | 二次加速，在开始时慢，随着时间推进加速，二次方增长。
    """

    out_quad = staticmethod(lambda x: 1 - (1 - x)**2)
    """
    | 二次减速，在开始时快速，随着时间推移减速，二次方衰减。
    """

    in_out_quad = staticmethod(lambda x: 2 * x**2 if x < 0.5 else 1 - (-2 * x + 2)**2 / 2.)
    """
    | 二次加减速，先加速然后减速，二次方的组合。
    """

    in_cubic = staticmethod(lambda x: x**3)
    """
    | 三次加速，在开始时非常慢，然后迅速加速，三次方增长。
    """

    out_cubic = staticmethod(lambda x: 1 - (1 - x)**3)
    """
    | 三次减速，在开始时快速，然后减速，三次方衰减。
    """

    in_out_cubic = staticmethod(lambda x: 4 * x**3 if x < 0.5 else 1 - (-2 * x + 2)**3 / 2.)
    """
    | 三次加减速，先加速然后减速，三次方的组合。
    """

    in_quart = staticmethod(lambda x: x**4)
    """
    | 四次加速，在开始时非常慢，然后迅速加速，四次方增长。
    """

    out_quart = staticmethod(lambda x: 1 - (1 - x)**4)
    """
    | 四次减速，在开始时非常快，然后逐渐减速，四次方衰减。
    """

    in_out_quart = staticmethod(lambda x: 8 * x**4 if x < 0.5 else 1 - (-2 * x + 2)**4 / 2.)
    """
    | 四次加减速，先加速然后减速，四次方的组合。
    """

    in_quint = staticmethod(lambda x: x**5)
    """
    | 五次加速，在开始时非常慢，然后急剧加速，五次方增长。
    """

    out_quint = staticmethod(lambda x: 1 - (1 - x)**5)
    """
    | 五次减速，在开始时非常快，随后减速，五次方衰减。
    """

    in_out_quint = staticmethod(lambda x: 16 * x**5 if x < 0.5 else 1 - (-2 * x + 2)**5 / 2.)
    """
    | 五次加减速，先加速然后减速，五次方的组合。
    """

    in_sine = staticmethod(lambda x: 1 - cos(x * pi / 2))
    """
    | 正弦加速，在开始时慢，随着时间加速，遵循正弦函数的形式。
    """

    out_sine = staticmethod(lambda x:  sin(x * pi / 2))
    """
    | 正弦减速，在开始时快，随后减速，遵循正弦函数的形式。
    """

    in_out_sine = staticmethod(lambda x: -0.5 * (cos(pi * x) - 1))
    """
    | 正弦加减速，先加速然后减速，遵循正弦函数的形式。
    """

    in_expo = staticmethod(lambda x: 0 if x == 0 else 2**(10 * (x - 1)))
    """
    | 指数加速，在开始时非常慢，随后迅速加速，遵循指数函数增长。
    """

    out_expo = staticmethod(lambda x: 1 if x == 1 else 1 - 2**(-10 * x))
    """
    | 指数减速，在开始时非常快，随后减速，遵循指数衰减。
    """

    @staticmethod
    def in_out_expo(x):
        """
        | 指数加减速，先加速然后减速，遵循指数函数。
        """
        if x == 0:
            return 0.
        if x == 1:
            return 1.
        return 2**(10 * (x * 2 - 1)) / 2. if x < 0.5 else (2 - 2**(-10 * (x * 2 - 1))) / 2.

    in_circ = staticmethod(lambda x: 1 - sqrt(1 - x**2))
    """
    | 圆形加速，在开始时较慢，然后加速，遵循圆形函数的效果。
    """

    out_circ = staticmethod(lambda x:  sqrt(1 - (x - 1)**2))
    """
    | 圆形减速，在开始时较快，然后减速，遵循圆形函数的效果。
    """

    in_out_circ = staticmethod(lambda x: 1 - sqrt(1 - (2 * x)**2) if x < 0.5 else sqrt(1 - (-2 * x + 2)**2) / 2.)
    """
    | 圆形加减速，先加速然后减速，遵循圆形函数的效果。
    """

    @staticmethod
    def in_bounce(x):
        """
        | 弹跳加速，表现为一种反复弹跳的加速效果。
        """
        return 1 - TimeEaseFunc.out_bounce(1 - x)

    @staticmethod
    def out_bounce(x):
        """
        | 弹跳减速，表现为一种弹跳的减速效果。
        """
        if x < 1 / 2.75:
            return 7.5625 * x**2
        elif x < 2 / 2.75:
            x -= 1.5 / 2.75
            return 7.5625 * x**2 + 0.75
        elif x < 2.5 / 2.75:
            x -= 2.25 / 2.75
            return 7.5625 * x**2 + 0.9375
        else:
            x -= 2.625 / 2.75
            return 7.5625 * x**2 + 0.984375

    @staticmethod
    def in_out_bounce(x):
        """
        | 弹跳加减速，先加速然后减速，表现为弹跳效果。
        """
        return 0.5 * TimeEaseFunc.in_bounce(x * 2) if x < 0.5 else 0.5 * TimeEaseFunc.out_bounce(x * 2 - 1) + 0.5

    in_back = staticmethod(lambda x: x**3 - x * sin(x * pi) * 1.70158)
    """
    | 回退加速，动画先稍微向后回退，然后加速。
    """

    out_back = staticmethod(lambda x: 1 - ((1 - x)**3 - (1 - x) * sin((1 - x) * pi) * 1.70158))
    """
    | 回退减速，动画开始时很快，之后回退并逐渐减速。
    """

    in_out_back = staticmethod(
        lambda x:
            (2 * x**3 - x * sin(x * pi) * 1.70158) if x < 0.5
            else (1 - ((2 - 2 * x)**3 - (2 - 2 * x) * sin((2 - 2 * x) * pi) * 1.70158))
    )
    """
    | 回退加减速，先回退后加速，之后回弹并减速。
    """

    in_elastic = staticmethod(lambda x: 1 - sin(6 * pi * x) * x**2)
    """
    | 弹性加速，具有弹性拉伸的效果，初期比较慢，然后加速。
    """

    out_elastic = staticmethod(lambda x:  sin(6 * pi * x) * (1 - x)**2)
    """
    | 弹性减速，弹性效果，快速运动然后逐渐回弹。
    """

    in_out_elastic = staticmethod(
        lambda x:
            (0.5 * (1 - sin(6 * pi * x) * x**2)) if x < 0.5
            else (0.5 * (sin(6 * pi * (x - 0.5)) * (1 - x)**2 + 1))
    )
    """
    | 弹性加减速，先加速后减速，表现为弹性效果。
    """


class TimeEase(object):
    """
    | 时间缓动对象。
    """

    def __init__(self, start_val, end_val, total_tm, fps=0, hold_on_last_frame=False, ease_func=TimeEaseFunc.linear):
        """
        | 创建一个时间缓动对象，内置各种时间缓动函数，可用于实现UI动画、运镜等的平滑过渡效果。
        | 时间缓动对象为一个迭代器，每次迭代或调用 ``next()`` 方法时，会返回一个新的缓动值。

        -----

        :param float start_val: 初始值
        :param float end_val: 最终值
        :param float total_tm: 变化总时间，单位为秒
        :param int fps: 变化帧率，小于等于0的值将根据实际时间确定缓动值，默认为0
        :param bool hold_on_last_frame: 是否停止在最后一帧；若设为True，TimeEase可无限迭代，变化结束后将始终返回最后一帧的值；若设为False，变化结束后继续迭代将抛出StopIteration异常；默认为False
        :param function ease_func: 时间缓动函数，可使用TimeEaseFunc提供的函数，或使用自定义函数，该函数接受并返回一个float值，且取值范围均为[0, 1]，默认为TimeEaseFunc.linear
        """
        self.start_val = start_val
        self.end_val = end_val
        self.total_tm = total_tm
        self.fps = fps
        self.hold_on_last_frame = hold_on_last_frame
        self.ease_func = ease_func
        self._init_tm = 0
        self._frame = 0
        self._total_frame = fps * total_tm
        self._stopped = False
        self._diff_val = self.end_val - self.start_val

    def __iter__(self):
        return self

    def next(self):
        if self._stopped and not self.hold_on_last_frame:
            raise StopIteration
        if self.fps > 0:
            x = min(self._frame / self._total_frame, 1)
            self._frame += 1
        else:
            if self._init_tm == 0:
                self._init_tm = time()
            x = min((time() - self._init_tm) / self.total_tm, 1)
        if x >= 1:
            self._stopped = True
        return self.start_val + self.ease_func(x) * self._diff_val

    def reset(self):
        """
        | 重置状态，重头开始计算。

        -----

        :return: 无
        :rtype: None
        """
        self._init_tm = 0
        self._frame = 0
        self._stopped = False

















