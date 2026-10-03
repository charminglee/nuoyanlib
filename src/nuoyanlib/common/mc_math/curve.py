# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-10-2
#  ⠀
#  ================================================


from __future__ import division
import bisect
import time as _time
from math import cos, floor, pi, sin, sqrt


__all__ = [
    "Curve",
    "CurveKey",
]


_UNSET = object()


def _looks_like_key_collection(value):
    if not isinstance(value, (list, tuple)):
        return False
    if not value:
        return True
    first = value[0]
    if isinstance(first, CurveKey):
        return True
    if isinstance(first, dict):
        return 'time' in first and 'value' in first
    return isinstance(first, (list, tuple)) and len(first) >= 2


class Curve(object):
    """
    标量曲线与支持迭代的时间动画。

    曲线有两种工作模式。使用 ``keys`` 创建的曲线会根据关键帧的绝对时间求值；
    未提供 ``keys`` 时， ``.eval_()`` 接收经过的秒数，并将其从 ``start_val`` 映射到 ``end_val`` 。
    曲线也可以通过 ``next()`` 逐帧迭代，或通过 ``.eval_()`` 在指定时间直接取值。

    示例
    ----

    创建一个使用固定帧率迭代的线性动画。设置 ``post_infinity=CONSTANT`` 后，动画结束时仍可继续调用 ``next``：

    >>> curve = Curve(
    ...     0.0, 10.0, total_time=2.0, fps=1,
    ...     post_infinity=Curve.Extrapolation.CONSTANT,
    ...     easing=Curve.Easing.LINEAR,
    ... )
    >>> [next(curve) for _ in range(4)]
    [0.0, 5.0, 10.0, 10.0]

    使用关键帧创建曲线，并设置时间范围外的循环方式：

    >>> curve = Curve.from_keys(
    ...     [(0.0, 0.0), (1.0, 10.0)],
    ...     post_infinity=Curve.Extrapolation.CYCLE,
    ... )
    >>> curve.eval_(0.25)
    2.5
    >>> curve.eval_(1.25)
    2.5

    可以通过 ``next`` 将多个动画连接起来：

    >>> fade_in = Curve(0.0, 1.0, 0.5, fps=10)
    >>> hold = Curve.static(1.0, 2.0)
    >>> fade_in.next = hold
    >>> next(fade_in)
    0.0

    -----

    :param float start_val: 初始值
    :param float end_val: 最终值
    :param float total_time: 变化总时间，单位为秒
    :param int fps: 变化帧率，小于等于 0 的值将根据现实时间确定缓动值；默认为 0
    :param function easing: 时间缓动函数，可使用 Curve 提供的预设函数或自定义函数，如 lambda x: x ；参数 x 表示经过的时间比例，取值范围为 [0, 1]；默认为 Curve.Easing.LINEAR
    :param Curve|None next: 下一个曲线对象；若提供，则当前曲线迭代结束后自动切换到下一个曲线继续迭代；默认为 None
    :param function|None on_start: 变化开始时触发的回调函数；默认为 None
    :param function|None on_end: 变化结束时触发的回调函数；默认为 None
    :param Sequence[CurveKey|tuple|list|dict]|None keys: 关键帧数据；支持 CurveKey 、 (time, value) 序列和包含 time -> value 的字典；默认为 None
    :param Curve.Extrapolation pre_infinity: 第一个关键帧之前的外推模式；默认为 Curve.Extrapolation.CONSTANT
    :param Curve.Extrapolation post_infinity: 最后一个关键帧之后的外推模式；默认为 Curve.Extrapolation.CONSTANT
    :param float default_value: 空关键帧曲线在 .eval_() 时使用的默认值；默认为 0.0
    """

    class Easing:
        LINEAR = staticmethod(lambda x: x)

        SPRING = staticmethod(lambda x: 1 - cos(x * pi * (0.2 + 2.5 * x ** 2)))

        IN_QUAD = staticmethod(lambda x: x ** 2)

        OUT_QUAD = staticmethod(lambda x: 1 - (1 - x) ** 2)

        IN_OUT_QUAD = staticmethod(
            lambda x:
            2 * x ** 2
            if x < 0.5
            else 1 - (-2 * x + 2) ** 2 / 2.
        )

        IN_CUBIC = staticmethod(lambda x: x**3)

        OUT_CUBIC = staticmethod(lambda x: 1 - (1 - x)**3)

        IN_OUT_CUBIC = staticmethod(
            lambda x:
                4 * x**3
                if x < 0.5
                else 1 - (-2 * x + 2)**3 / 2.
        )

        IN_QUART = staticmethod(lambda x: x**4)

        OUT_QUART = staticmethod(lambda x: 1 - (1 - x)**4)

        IN_OUT_QUART = staticmethod(
            lambda x:
                8 * x**4
                if x < 0.5
                else 1 - (-2 * x + 2)**4 / 2.
        )

        IN_QUINT = staticmethod(lambda x: x**5)

        OUT_QUINT = staticmethod(lambda x: 1 - (1 - x)**5)

        IN_OUT_QUINT = staticmethod(
            lambda x:
                16 * x**5
                if x < 0.5
                else 1 - (-2 * x + 2)**5 / 2.
        )

        IN_SINE = staticmethod(lambda x: 1 - cos(x * pi / 2))

        OUT_SINE = staticmethod(lambda x: sin(x * pi / 2))

        IN_OUT_SINE = staticmethod(lambda x: -0.5 * (cos(pi * x) - 1))

        IN_EXPO = staticmethod(
            lambda x:
                0
                if x == 0
                else 2**(10 * (x - 1))
        )

        OUT_EXPO = staticmethod(
            lambda x:
                1
                if x == 1
                else 1 - 2**(-10 * x)
        )

        @staticmethod
        def IN_OUT_EXPO(x):
            if x == 0:
                return 0.
            if x == 1:
                return 1.
            return (
                2**(10 * (x * 2 - 1)) / 2.
                if x < 0.5
                else (2 - 2**(-10 * (x * 2 - 1))) / 2.
            )

        IN_CIRC = staticmethod(lambda x: 1 - sqrt(1 - x**2))

        OUT_CIRC = staticmethod(lambda x: sqrt(1 - (x - 1)**2))

        IN_OUT_CIRC = staticmethod(
            lambda x:
                1 - sqrt(1 - (2 * x)**2)
                if x < 0.5
                else sqrt(1 - (-2 * x + 2)**2) / 2.
        )

        @staticmethod
        def IN_BACK(x):
            c1 = 1.70158
            c3 = c1 + 1
            return c3 * x**3 - c1 * x**2

        @staticmethod
        def OUT_BACK(x):
            c1 = 1.70158
            c3 = c1 + 1
            return 1 + c3 * (x - 1)**3 + c1 * (x - 1)**2

        @staticmethod
        def IN_OUT_BACK(x):
            c1 = 1.70158
            c2 = c1 * 1.525
            return (
                ((2 * x)**2 * ((c2 + 1) * 2 * x - c2)) / 2
                if x < 0.5
                else ((2 * x - 2)**2 * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
            )

        @staticmethod
        def IN_ELASTIC(x):
            if x == 0:
                return 0.
            if x == 1:
                return 1.
            return -2 ** (10 * x - 10) * sin((10 * x - 10.75) * (2 * pi / 3))

        @staticmethod
        def OUT_ELASTIC(x):
            if x == 0:
                return 0.
            if x == 1:
                return 1.
            return 2 ** (-10 * x) * sin((10 * x - 0.75) * (2 * pi / 3)) + 1

        @staticmethod
        def IN_OUT_ELASTIC(x):
            if x == 0:
                return 0.
            if x == 1:
                return 1.
            c5 = 2 * pi / 4.5
            return (
                -(2 ** (20 * x - 10) * sin((20 * x - 11.125) * c5)) / 2
                if x < 0.5
                else (2 ** (-20 * x + 10) * sin((20 * x - 11.125) * c5)) / 2 + 1
            )

        @staticmethod
        def IN_BOUNCE(x):
            return 1 - Curve.Easing.OUT_BOUNCE(1 - x)

        @staticmethod
        def OUT_BOUNCE(x):
            if x < 1 / 2.75:
                return 7.5625 * x ** 2
            if x < 2 / 2.75:
                x -= 1.5 / 2.75
                return 7.5625 * x ** 2 + 0.75
            if x < 2.5 / 2.75:
                x -= 2.25 / 2.75
                return 7.5625 * x ** 2 + 0.9375
            x -= 2.625 / 2.75
            return 7.5625 * x ** 2 + 0.984375

        @staticmethod
        def IN_OUT_BOUNCE(x):
            return (
                0.5 * Curve.Easing.IN_BOUNCE(x * 2)
                if x < 0.5
                else 0.5 * Curve.Easing.OUT_BOUNCE(x * 2 - 1) + 0.5
            )

    class InterpMode:
        """
        关键帧之间的插值模式。

        插值模式由前一个关键帧控制当前关键帧与下一个关键帧之间的曲线形状。

        - ``CONSTANT`` -- 保持前一个关键帧的值。
        - ``LINEAR`` -- 线性插值。
        - ``CUBIC`` -- 使用关键帧切线进行三次 Hermite 插值。
        """

        CONSTANT = "constant"
        LINEAR = "linear"
        CUBIC = "cubic"

    class TangentMode:
        """
        关键帧切线的计算模式。

        - ``AUTO`` -- 根据相邻关键帧自动计算切线。
        - ``AUTO_CLAMPED`` -- 额外限制切线以减少过冲。
        - ``USER`` -- 使用 arrive_tangent 和 leave_tangent 。
        - ``BREAK`` -- 允许到达和离开切线独立设置。
        - ``NONE`` -- 将切线视为 0 。
        """

        NONE = "none"
        AUTO = "auto"
        USER = "user"
        BREAK = "break"
        AUTO_CLAMPED = "auto_clamped"

    class WeightedMode:
        """
        关键帧切线权重的标记。

        ``arrive_weight`` 和 ``leave_weight`` 会随关键帧保存，便于兼容带权重的曲线数据。
        当前曲线求值使用普通三次 Hermite 插值，权重不会改变求值结果。
        """

        NONE = "none"
        ARRIVE = "arrive"
        LEAVE = "leave"
        BOTH = "both"

    class Extrapolation:
        """
        关键帧时间范围之外的外推模式。

        - ``CONSTANT`` -- 保持边界值。
        - ``LINEAR`` -- 按边界切线延伸。
        - ``CYCLE`` -- 循环播放。
        - ``CYCLE_WITH_OFFSET`` -- 循环播放并叠加每一周期的首尾值差。
        - ``OSCILLATE`` -- 在正向与反向之间交替播放。
        """

        CONSTANT = "constant"
        LINEAR = "linear"
        CYCLE = "cycle"
        CYCLE_WITH_OFFSET = "cycle_with_offset"
        OSCILLATE = "oscillate"

    def __init__(
            self,
            start_val=0.0,
            end_val=1.0,
            total_time=1.0,
            fps=0,
            easing=Easing.LINEAR,
            next=None,
            on_start=None,
            on_end=None,
            keys=None,
            pre_infinity=Extrapolation.CONSTANT,
            post_infinity=Extrapolation.CONSTANT,
            default_value=0.0,
    ):
        if keys is None and _looks_like_key_collection(start_val) and end_val == 1.0 and total_time == 1.0:
            keys = start_val
            start_val = 0.0
            end_val = 1.0
            total_time = 1.0

        self.start_val = float(start_val)
        self.end_val = float(end_val)
        self.total_time = float(total_time)
        self.fps = int(fps)
        self.easing = easing
        self.next_curve = next
        self.on_start = on_start
        self.on_end = on_end
        self.default_value = float(default_value)
        self.pre_infinity = pre_infinity
        self.post_infinity = post_infinity

        self._keys = []
        self._key_mode = keys is not None
        self._next_handle = 1
        self._init_tm = 0
        self._frame = 0
        self._total_frame = 0
        self._diff_val = self.end_val - self.start_val
        self._val = self.start_val
        self._state = 0
        self._is_static = False

        if keys is not None:
            for key in keys:
                self.add_key(key)
        self._refresh_total_frame()
        self._val = self._initial_value()

    @classmethod
    def from_keys(
            cls,
            keys,
            pre_infinity=Extrapolation.CONSTANT,
            post_infinity=Extrapolation.CONSTANT,
            default_value=0.0,
    ):
        """
        [类方法]

        从关键帧数据创建曲线。

        示例
        ----

        >>> curve = Curve.from_keys(
        ...     [(0.0, 0.0), (1.0, 1.0)],
        ...     post_infinity=Curve.Extrapolation.LINEAR,
        ... )
        >>> curve.eval_(0.5)
        0.5

        关键帧会按 ``time`` 升序保存，关键帧之间默认使用三次插值。

        -----

        :param Sequence[CurveKey|tuple|list|dict] keys: 关键帧数据
        :param Curve.Extrapolation pre_infinity: 第一个关键帧之前的外推模式；默认为 Curve.Extrapolation.CONSTANT
        :param Curve.Extrapolation post_infinity: 最后一个关键帧之后的外推模式；默认为 Curve.Extrapolation.CONSTANT
        :param float default_value: 空关键帧曲线的默认值；默认为 0.0

        :return: 关键帧曲线
        :rtype: Curve
        """
        return cls(
            keys=keys,
            pre_infinity=pre_infinity,
            post_infinity=post_infinity,
            default_value=default_value,
        )

    @classmethod
    def static(
            cls,
            val,
            total_time,
            next=None,
            on_start=None,
            on_end=None,
    ):
        """
        [类方法]

        创建在整个持续时间内保持同一值的静态曲线。

        示例
        ----

        >>> curve = Curve.static(3.0, total_time=1.0)
        >>> curve.eval_(0.5)
        3.0
        >>> curve.next = Curve.static(4.0, total_time=1.0)

        :param float val: 静态值
        :param float total_time: 持续时间，单位为秒
        :param Curve|None next: 下一个曲线对象；默认为 None
        :param function|None on_start: 变化开始时触发的回调函数；默认为 None
        :param function|None on_end: 变化结束时触发的回调函数；默认为 None
        :return: 静态曲线
        :rtype: Curve
        """
        curve = cls(
            val,
            val,
            total_time,
            next=next,
            on_start=on_start,
            on_end=on_end,
        )
        curve._val = float(val)
        curve._is_static = True
        return curve

    @property
    def keys(self):
        """
        [可读写属性]

        获取或替换当前曲线的关键帧列表。读取时返回 ``CurveKey`` 列表；
        赋值为 ``None`` 会切换回普通时间缓动模式，赋值为序列则切换为关键帧模式。

        示例
        ----

        >>> curve = Curve()
        >>> curve.keys = [(0.0, 0.0), (1.0, 1.0)]
        >>> curve.keys[0].time
        0.0

        :return: 当前关键帧列表
        :rtype: list[CurveKey]
        """
        return self._keys

    @keys.setter
    def keys(self, values):
        self.clear()
        self._key_mode = values is not None
        if values is not None:
            for key in values:
                self.add_key(key)

    @property
    def duration(self):
        """
        [只读属性]

        获取曲线持续时间。关键帧模式下为首尾关键帧时间差，普通模式下为 ``total_time``；结果不会小于 0。

        :return: 曲线持续时间，单位为秒
        :rtype: float
        """
        if self._keys:
            return max(self._keys[-1].time - self._keys[0].time, 0.0)
        return max(self.total_time, 0.0)

    @property
    def first_key_time(self):
        """
        [只读属性]

        获取第一个关键帧的时间。没有关键帧时返回 ``0.0`` 。

        :return: 第一个关键帧时间
        :rtype: float
        """
        return self._keys[0].time if self._keys else 0.0

    @property
    def last_key_time(self):
        """
        [只读属性]

        获取最后一个关键帧的时间。没有关键帧时返回 ``0.0`` 。

        :return: 最后一个关键帧时间
        :rtype: float
        """
        return self._keys[-1].time if self._keys else 0.0

    @property
    def finished(self):
        """
        [只读属性]

        判断曲线是否已经迭代结束。

        :return: 是否已结束
        :rtype: bool
        """
        return self._state == 2

    def _refresh_total_frame(self):
        if self.fps > 0:
            self._total_frame = max(int(self.fps * self.duration), 1)
        else:
            self._total_frame = 0

    def _initial_value(self):
        if self._keys:
            return self._keys[0].value
        return self.start_val

    def _coerce_key(self, key_or_time, value=_UNSET, **kwargs):
        if isinstance(key_or_time, CurveKey):
            return key_or_time
        if isinstance(key_or_time, dict):
            data = dict(key_or_time)
            return CurveKey(
                data.pop('time'),
                data.pop('value'),
                data.pop('arrive_tangent', 0.0),
                data.pop('leave_tangent', 0.0),
                data.pop('interp_mode', Curve.InterpMode.CUBIC),
                data.pop('tangent_mode', Curve.TangentMode.AUTO),
                data.pop('arrive_weight', 1.0),
                data.pop('leave_weight', 1.0),
                data.pop('weighted_mode', Curve.WeightedMode.NONE),
            )
        if value is _UNSET:
            if isinstance(key_or_time, (list, tuple)) and len(key_or_time) >= 2:
                values = list(key_or_time)
                return CurveKey(
                    values[0],
                    values[1],
                    values[2] if len(values) > 2 else 0.0,
                    values[3] if len(values) > 3 else 0.0,
                    values[4] if len(values) > 4 else Curve.InterpMode.CUBIC,
                    values[5] if len(values) > 5 else Curve.TangentMode.AUTO,
                )
            raise TypeError("a curve key requires both time and value")
        return CurveKey(key_or_time, value, **kwargs)

    def add_key(
            self,
            key_or_time,
            value=_UNSET,
            arrive_tangent=0.0,
            leave_tangent=0.0,
            interp_mode=InterpMode.CUBIC,
            tangent_mode=TangentMode.AUTO,
            arrive_weight=1.0,
            leave_weight=1.0,
            weighted_mode=WeightedMode.NONE,
    ):
        """
        添加一个关键帧。

        ``key_or_time`` 可以是 ``CurveKey`` 、包含至少两个元素的序列、包含 ``time`` 和 ``value`` 的字典，也可以直接传入关键帧时间并通过 ``value`` 传入值。
        关键帧会自动按时间升序插入。

        示例
        ----

        >>> curve = Curve()
        >>> first = curve.add_key(0.0, 0.0, interp_mode=Curve.InterpMode.LINEAR)
        >>> second = curve.add_key({"time": 1.0, "value": 10.0})
        >>> curve.eval_(0.25)
        2.5
        >>> first.handle < second.handle
        True

        -----

        :param CurveKey|tuple|list|dict|float key_or_time: 关键帧对象、关键帧数据或时间
        :param float|None value: 关键帧值；当 key_or_time 为时间时必须传入
        :param float arrive_tangent: 到达切线；默认为 0.0
        :param float leave_tangent: 离开切线；默认为 0.0
        :param Curve.InterpMode interp_mode: 插值模式；默认为 Curve.InterpMode.CUBIC
        :param Curve.TangentMode tangent_mode: 切线模式；默认为 Curve.TangentMode.AUTO
        :param float arrive_weight: 到达切线权重；默认为 1.0
        :param float leave_weight: 离开切线权重；默认为 1.0
        :param Curve.WeightedMode weighted_mode: 切线权重标记；默认为 Curve.WeightedMode.NONE

        :return: 新添加的关键帧
        :rtype: CurveKey

        :raise TypeError: ``key_or_time`` 未提供合法的关键帧值时抛出
        """
        self._key_mode = True
        if isinstance(key_or_time, (CurveKey, dict)) or value is _UNSET:
            key = self._coerce_key(key_or_time, value)
        else:
            key = CurveKey(
                key_or_time,
                value,
                arrive_tangent,
                leave_tangent,
                interp_mode,
                tangent_mode,
                arrive_weight,
                leave_weight,
                weighted_mode,
            )
        key._handle = self._next_handle
        self._next_handle += 1
        times = [item.time for item in self._keys]
        self._keys.insert(bisect.bisect_right(times, key.time), key)
        self._refresh_total_frame()
        return key

    def update_or_add_key(self, key_time, value, **kwargs):
        """
        更新指定时间的关键帧；找不到时添加新关键帧。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 0.0)])
        >>> curve.update_or_add_key(0.0, 2.0)
        CurveKey(time=0.0, value=2.0)
        >>> curve.update_or_add_key(1.0, 4.0)
        CurveKey(time=1.0, value=4.0)

        :param float key_time: 关键帧时间
        :param float value: 关键帧值
        :param dict kwargs: 传递给 update_key 或 add_key 的其他关键帧属性

        :return: 更新或新添加的关键帧
        :rtype: CurveKey
        """
        key = self.find_key(key_time)
        if key is None:
            return self.add_key(key_time, value, **kwargs)
        self.update_key(key, value=value, **kwargs)
        return key

    def _resolve_key(self, key):
        if isinstance(key, CurveKey):
            if key in self._keys:
                return key
            key = key.handle
        if isinstance(key, int):
            for item in self._keys:
                if item.handle == key:
                    return item
            if 0 <= key < len(self._keys):
                return self._keys[key]
            return None
        if isinstance(key, float):
            return self.find_key(key)
        return None

    def find_key(self, key_time, tolerance=1e-6):
        """
        按时间查找关键帧。

        当多个关键帧处于容差范围内时，返回最后添加且匹配的关键帧。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 1.0), (1.0, 2.0)])
        >>> curve.find_key(1.0).value
        2.0
        >>> curve.find_key(1.0001, tolerance=1e-3).value
        2.0

        :param float|CurveKey key_time: 关键帧时间或关键帧对象
        :param float tolerance: 时间匹配容差；默认为 1e-6

        :return: 匹配的关键帧；找不到时返回 None
        :rtype: CurveKey|None
        """
        if isinstance(key_time, CurveKey):
            return self._resolve_key(key_time)
        target = float(key_time)
        for key in reversed(self._keys):
            if abs(key.time - target) <= tolerance:
                return key
        return None

    def get_key(self, key):
        """
        获取指定的关键帧。

        ``key`` 可以是关键帧对象、由 ``Curve`` 分配的句柄、关键帧列表索引或时间。

        :param CurveKey|int|float key: 关键帧对象、句柄、索引或时间

        :return: 匹配的关键帧；找不到时返回 None
        :rtype: CurveKey|None
        """
        return self._resolve_key(key)

    def get_keys(self):
        """
        获取当前曲线的关键帧列表拷贝。

        与 ``keys`` 属性不同，返回的新列表可以安全地修改而不会改变曲线中的列表；
        但列表中的 ``CurveKey`` 对象仍然是曲线中的对象。

        :return: 关键帧列表拷贝
        :rtype: list[CurveKey]
        """
        return list(self._keys)

    def update_key(
            self,
            key,
            time=None,
            value=None,
            arrive_tangent=None,
            leave_tangent=None,
            interp_mode=None,
            tangent_mode=None,
            arrive_weight=None,
            leave_weight=None,
            weighted_mode=None,
    ):
        """
        更新指定关键帧的属性。

        未传入的属性保持不变。修改时间后，曲线会重新按时间排序。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 0.0), (1.0, 1.0)])
        >>> key = curve.find_key(1.0)
        >>> curve.update_key(
        ...     key, value=2.0, interp_mode=Curve.InterpMode.LINEAR,
        ... )
        CurveKey(time=1.0, value=2.0)
        >>> key.value
        2.0

        -----

        :param CurveKey|int|float key: 关键帧对象、句柄、索引或时间
        :param float|None time: 新时间；默认为 None，表示不修改
        :param float|None value: 新值；默认为 None，表示不修改
        :param float|None arrive_tangent: 新到达切线；默认为 None，表示不修改
        :param float|None leave_tangent: 新离开切线；默认为 None，表示不修改
        :param Curve.InterpMode|None interp_mode: 新插值模式；默认为 None，表示不修改
        :param Curve.TangentMode|None tangent_mode: 新切线模式；默认为 None，表示不修改
        :param float|None arrive_weight: 新到达切线权重；默认为 None，表示不修改
        :param float|None leave_weight: 新离开切线权重；默认为 None，表示不修改
        :param Curve.WeightedMode|None weighted_mode: 新切线权重标记；默认为 None，表示不修改

        :return: 更新后的关键帧；关键帧不存在时返回 None
        :rtype: CurveKey|None
        """
        key = self._resolve_key(key)
        if key is None:
            return None
        if time is not None:
            key.time = float(time)
        if value is not None:
            key.value = float(value)
        if arrive_tangent is not None:
            key.arrive_tangent = float(arrive_tangent)
        if leave_tangent is not None:
            key.leave_tangent = float(leave_tangent)
        if interp_mode is not None:
            key.interp_mode = interp_mode
        if tangent_mode is not None:
            key.tangent_mode = tangent_mode
        if arrive_weight is not None:
            key.arrive_weight = float(arrive_weight)
        if leave_weight is not None:
            key.leave_weight = float(leave_weight)
        if weighted_mode is not None:
            key.weighted_mode = weighted_mode
        self._keys.sort(key=lambda item: (item.time, item.handle or 0))
        self._refresh_total_frame()
        return key

    def set_key_tangents(self, key, arrive_tangent, leave_tangent=None):
        """
        设置关键帧切线，并将切线模式设置为 ``Curve.TangentMode.USER`` 。

        省略 ``leave_tangent`` 时，离开切线与到达切线相同。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 0.0), (1.0, 1.0)])
        >>> curve.set_key_tangents(0, 1.0)
        CurveKey(time=0.0, value=0.0)

        :param CurveKey|int|float key: 关键帧对象、句柄、索引或时间
        :param float arrive_tangent: 到达切线
        :param float|None leave_tangent: 离开切线；默认为 None，表示使用到达切线

        :return: 更新后的关键帧；关键帧不存在时返回 None
        :rtype: CurveKey|None
        """
        if leave_tangent is None:
            leave_tangent = arrive_tangent
        return self.update_key(
            key,
            arrive_tangent=arrive_tangent,
            leave_tangent=leave_tangent,
            tangent_mode=Curve.TangentMode.USER,
        )

    def delete_key(self, key):
        """
        删除指定关键帧。

        ``key`` 可以是关键帧对象、句柄、关键帧列表索引或时间。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 0.0), (1.0, 1.0)])
        >>> curve.delete_key(0)
        True
        >>> curve.is_empty()
        False

        :param CurveKey|int|float key: 关键帧对象、句柄、索引或时间

        :return: 是否成功删除
        :rtype: bool
        """
        key = self._resolve_key(key)
        if key is None:
            return False
        self._keys.remove(key)
        self._refresh_total_frame()
        return True

    def clear(self):
        """
        清空当前曲线的所有关键帧。

        对于关键帧模式的曲线，清空后仍处于关键帧模式；此时 ``.eval_()`` 会返回 ``default_value``，或返回调用时传入的 ``default_value`` 。

        :return: 无
        :rtype: None
        """
        self._keys[:] = []
        self._refresh_total_frame()

    def is_empty(self):
        """
        判断当前曲线是否没有关键帧。

        :return: 是否为空
        :rtype: bool
        """
        return not self._keys

    def is_constant(self):
        """
        判断关键帧是否全部具有相同的值。

        少于两个关键帧时返回 True。

        :return: 是否为常量曲线
        :rtype: bool
        """
        if len(self._keys) < 2:
            return True
        value = self._keys[0].value
        return all(key.value == value for key in self._keys[1:])

    def get_time_range(self):
        """
        获取曲线的时间范围。

        有关键帧时返回首个和最后一个关键帧的时间；没有关键帧时返回 ``(0.0, duration)`` 。

        :return: 最小时间和最大时间
        :rtype: tuple[float, float]
        """
        if not self._keys:
            return 0.0, self.duration
        return self.first_key_time, self.last_key_time

    def get_value_range(self):
        """
        获取曲线关键帧值的范围。

        有关键帧时返回所有关键帧值的最小值和最大值；没有关键帧时返回 ``start_val`` 与 ``end_val`` 的范围。

        :return: 最小值和最大值
        :rtype: tuple[float, float]
        """
        if not self._keys:
            return min(self.start_val, self.end_val), max(self.start_val, self.end_val)
        values = [key.value for key in self._keys]
        return min(values), max(values)

    def set_pre_infinity(self, mode):
        """
        设置第一个关键帧之前的外推模式。

        示例
        ----

        >>> curve = Curve.from_keys([(0.0, 0.0), (1.0, 1.0)])
        >>> curve.set_pre_infinity(Curve.Extrapolation.LINEAR) is curve
        True
        >>> curve.pre_infinity
        'linear'

        :param Curve.Extrapolation mode: 外推模式

        :return: 当前曲线
        :rtype: Curve
        """
        self.pre_infinity = mode
        return self

    def set_post_infinity(self, mode):
        """
        设置最后一个关键帧之后的外推模式。

        :param Curve.Extrapolation mode: 外推模式

        :return: 当前曲线
        :rtype: Curve
        """
        self.post_infinity = mode
        return self

    def _auto_tangent(self, index, clamped=False):
        if len(self._keys) < 2:
            return 0.0
        if index == 0:
            next_key = self._keys[1]
            dt = next_key.time - self._keys[0].time
            return (next_key.value - self._keys[0].value) / dt if dt else 0.0
        if index == len(self._keys) - 1:
            previous_key = self._keys[-2]
            dt = self._keys[-1].time - previous_key.time
            return (self._keys[-1].value - previous_key.value) / dt if dt else 0.0

        previous_key = self._keys[index - 1]
        key = self._keys[index]
        next_key = self._keys[index + 1]
        previous_dt = key.time - previous_key.time
        next_dt = next_key.time - key.time
        previous_slope = (key.value - previous_key.value) / previous_dt if previous_dt else 0.0
        next_slope = (next_key.value - key.value) / next_dt if next_dt else 0.0
        if clamped:
            if previous_slope == 0 or next_slope == 0 or previous_slope * next_slope <= 0:
                return 0.0
            sign = 1 if previous_slope > 0 else -1
            return sign * min(abs(previous_slope), abs(next_slope))
        total_dt = next_key.time - previous_key.time
        return (next_key.value - previous_key.value) / total_dt if total_dt else 0.0

    def _tangent(self, index, side):
        key = self._keys[index]
        mode = key.tangent_mode
        if mode == Curve.TangentMode.NONE:
            return 0.0
        if mode in (Curve.TangentMode.USER, Curve.TangentMode.BREAK):
            return key.arrive_tangent if side == "arrive" else key.leave_tangent
        return self._auto_tangent(index, mode == Curve.TangentMode.AUTO_CLAMPED)

    def _linear_slope(self, index, side):
        key = self._keys[index]
        tangent_mode = key.tangent_mode
        if tangent_mode == Curve.TangentMode.NONE:
            return 0.0
        if tangent_mode in (Curve.TangentMode.USER, Curve.TangentMode.BREAK):
            return key.arrive_tangent if side == "arrive" else key.leave_tangent
        if side == "arrive":
            other = self._keys[index - 1] if index else self._keys[index + 1]
        else:
            other = self._keys[index + 1] if index < len(self._keys) - 1 else self._keys[index - 1]
        dt = key.time - other.time
        return (key.value - other.value) / dt if dt else 0.0

    def _eval_in_range(self, at_time):
        if len(self._keys) == 1:
            return self._keys[0].value
        times = [key.time for key in self._keys]
        index = bisect.bisect_right(times, at_time) - 1
        if index < 0:
            return self._keys[0].value
        if index >= len(self._keys) - 1:
            return self._keys[-1].value

        first = self._keys[index]
        second = self._keys[index + 1]
        dt = second.time - first.time
        if dt <= 0:
            return second.value
        alpha = (at_time - first.time) / dt
        mode = first.interp_mode
        if mode == Curve.InterpMode.CONSTANT:
            return first.value
        if mode == Curve.InterpMode.LINEAR:
            return first.value + (second.value - first.value) * alpha

        alpha2 = alpha * alpha
        alpha3 = alpha2 * alpha
        h00 = 2 * alpha3 - 3 * alpha2 + 1
        h10 = alpha3 - 2 * alpha2 + alpha
        h01 = -2 * alpha3 + 3 * alpha2
        h11 = alpha3 - alpha2
        first_tangent = self._tangent(index, "leave")
        second_tangent = self._tangent(index + 1, "arrive")
        return (
                h00 * first.value
                + h10 * dt * first_tangent
                + h01 * second.value
                + h11 * dt * second_tangent
        )

    def _eval_outside(self, at_time, before):
        first = self._keys[0]
        last = self._keys[-1]
        mode = self.pre_infinity if before else self.post_infinity
        if mode == Curve.Extrapolation.CONSTANT:
            return first.value if before else last.value
        if mode == Curve.Extrapolation.LINEAR:
            if before:
                return first.value + (at_time - first.time) * self._linear_slope(0, "arrive")
            return last.value + (at_time - last.time) * self._linear_slope(len(self._keys) - 1, "leave")

        duration = last.time - first.time
        if duration <= 0:
            return first.value
        cycle = int(floor((at_time - first.time) / duration))
        local_time = at_time - cycle * duration
        if local_time < first.time:
            local_time = first.time
        elif local_time > last.time:
            local_time = last.time
        if mode == Curve.Extrapolation.OSCILLATE and cycle % 2:
            local_time = first.time + last.time - local_time
        value = self._eval_in_range(local_time)
        if mode == Curve.Extrapolation.CYCLE_WITH_OFFSET:
            value += cycle * (last.value - first.value)
        return value

    def _eval_keyframes(self, at_time):
        first = self._keys[0]
        last = self._keys[-1]
        if at_time < first.time:
            return self._eval_outside(at_time, True)
        if at_time > last.time:
            return self._eval_outside(at_time, False)
        return self._eval_in_range(at_time)

    def eval_(self, at_time, default_value=None):
        """
        在指定时间计算曲线值。

        普通时间缓动模式下，``at_time`` 是从 0 开始计算的经过时间，并会被限制在 ``[0, total_time]`` ；
        关键帧模式下， ``at_time`` 是关键帧使用的绝对时间，超出关键帧范围的部分由外推模式处理。

        示例
        ----

        >>> curve = Curve(10.0, 20.0, total_time=2.0, easing=Curve.Easing.LINEAR)
        >>> curve.eval_(1.0)
        15.0
        >>> key_curve = Curve.from_keys([(0.0, 0.0), (2.0, 8.0)])
        >>> key_curve(1.0)
        4.0

        空关键帧曲线会返回曲线的 ``default_value`` ；调用时传入的默认值优先级更高。

        -----

        :param float at_time: 求值时间
        :param float|None default_value: 空关键帧曲线的临时默认值；默认为 None，表示使用曲线的 default_value

        :return: 曲线值
        :rtype: float
        """
        if self._key_mode:
            if not self._keys:
                return self.default_value if default_value is None else default_value
            return self._eval_keyframes(float(at_time))

        if self.total_time <= 0:
            progress = 1.0
        else:
            progress = max(0.0, min(float(at_time) / self.total_time, 1.0))
        if self._is_static:
            return self.start_val
        return self.start_val + self.easing(progress) * self._diff_val

    get_value = __call__ = eval_

    def _animation_value(self, progress):
        if self._key_mode:
            if not self._keys:
                return self.default_value
            return self._eval_keyframes(
                self.first_key_time + progress * self.duration
            )
        if self._is_static:
            return self.start_val
        return self.start_val + self.easing(progress) * self._diff_val

    def __iter__(self):
        return self

    def _on_start(self):
        self._state = 1
        if self.on_start:
            self.on_start()

    def _on_end(self):
        if self.on_end:
            self.on_end()
        self._state = 2
        if self.next_curve:
            next_curve = self.next_curve
            self.start_val = next_curve.start_val
            self.end_val = next_curve.end_val
            self.total_time = next_curve.total_time
            self.fps = next_curve.fps
            self.easing = next_curve.easing
            self.on_start = next_curve.on_start
            self.on_end = next_curve.on_end
            self.default_value = next_curve.default_value
            self.pre_infinity = next_curve.pre_infinity
            self.post_infinity = next_curve.post_infinity
            self._keys = list(next_curve._keys)
            self._key_mode = next_curve._key_mode
            self._next_handle = next_curve._next_handle
            self._is_static = next_curve._is_static
            self._val = next_curve._val
            self.next_curve = next_curve.next_curve
            self.reset()

    def __next__(self):
        """
        获取下一帧的曲线值。

        当 ``fps`` 大于 ``0`` 时按固定帧率推进；当 ``fps`` 小于等于 ``0`` 时根据现实时间推进。
        动画结束后， ``post_infinity`` 为 ``CONSTANT`` 时持续返回最后一帧，否则抛出 ``StopIteration``。

        示例
        ----

        >>> curve = Curve(
        ...     0.0,
        ...     1.0,
        ...     total_time=1.0,
        ...     fps=1,
        ...     post_infinity=Curve.Extrapolation.LINEAR,
        ... )
        >>> next(curve)
        0.0
        >>> next(curve)
        1.0
        >>> next(curve)
        Traceback (most recent call last):
        ...
        StopIteration

        :return: 当前帧的曲线值
        :rtype: float

        :raise StopIteration: 曲线结束且 ``post_infinity`` 不是 ``CONSTANT`` 时抛出
        """
        if self._state == 0:
            self._on_start()
        elif self._state == 2:
            if self.post_infinity == Curve.Extrapolation.CONSTANT:
                return self._val
            raise StopIteration

        duration = self.duration
        if duration <= 0:
            progress = 1.0
        elif self.fps > 0:
            progress = min(self._frame / float(self._total_frame), 1.0)
            self._frame += 1
        else:
            if self._init_tm == 0:
                self._init_tm = _time.time()
            elapsed = _time.time() - self._init_tm
            progress = min(max(elapsed / duration, 0.0), 1.0)

        self._val = self._animation_value(progress)
        if progress >= 1:
            self._on_end()
        return self._val

    next = __next__

    def reset(self):
        """
        重置曲线迭代状态。

        重置后会从第一帧重新开始迭代；关键帧、回调和外推模式等曲线配置不会改变。

        示例
        ----

        >>> curve = Curve(0.0, 1.0, total_time=1.0, fps=1)
        >>> next(curve)
        0.0
        >>> next(curve)
        1.0
        >>> curve.reset()
        >>> next(curve)
        0.0

        :return: 无
        :rtype: None
        """
        self._init_tm = 0
        self._frame = 0
        self._state = 0
        self._diff_val = self.end_val - self.start_val
        self._refresh_total_frame()
        self._val = self._initial_value()

    def copy(self):
        """
        创建当前曲线的拷贝。

        示例
        ----

        >>> curve = Curve(0.0, 1.0, total_time=1.0)
        >>> copied = curve.copy()
        >>> (copied.start_val, copied.end_val, copied.total_time)
        (0.0, 1.0, 1.0)

        -----

        :return: 曲线拷贝
        :rtype: Curve
        """
        curve = Curve(
            start_val=self.start_val,
            end_val=self.end_val,
            total_time=self.total_time,
            fps=self.fps,
            easing=self.easing,
            next=self.next_curve,
            on_start=self.on_start,
            on_end=self.on_end,
            pre_infinity=self.pre_infinity,
            post_infinity=self.post_infinity,
            default_value=self.default_value,
        )
        curve._keys = [key.copy() for key in self._keys]
        curve._key_mode = self._key_mode
        curve._next_handle = self._next_handle
        curve._refresh_total_frame()
        curve._val = curve._initial_value()
        curve._is_static = self._is_static
        return curve

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy()


class CurveKey(object):
    """
    标量曲线关键帧。

    关键帧包含时间、值、插值模式以及切线信息。将关键帧加入 ``Curve`` 后， ``Curve`` 会按时间升序保存它们，并为关键帧分配 ``handle`` 。

    示例
    ----

    >>> key = CurveKey(0.5, 10.0, interp_mode=Curve.InterpMode.LINEAR)
    >>> (key.time, key.value)
    (0.5, 10.0)

    -----

    :param float time: 关键帧时间
    :param float value: 关键帧值
    :param float arrive_tangent: 到达关键帧时的切线；默认为 0.0
    :param float leave_tangent: 离开关键帧时的切线；默认为 0.0
    :param Curve.InterpMode interp_mode: 插值模式；默认为 Curve.InterpMode.CUBIC
    :param Curve.TangentMode tangent_mode: 切线模式；默认为 Curve.TangentMode.AUTO
    :param float arrive_weight: 到达切线权重；默认为 1.0
    :param float leave_weight: 离开切线权重；默认为 1.0
    :param Curve.WeightedMode weighted_mode: 切线权重标记；默认为 Curve.WeightedMode.NONE
    """

    def __init__(
            self,
            time,
            value,
            arrive_tangent=0.0,
            leave_tangent=0.0,
            interp_mode=Curve.InterpMode.CUBIC,
            tangent_mode=Curve.TangentMode.AUTO,
            arrive_weight=1.0,
            leave_weight=1.0,
            weighted_mode=Curve.WeightedMode.NONE,
    ):
        self.time = float(time)
        self.value = float(value)
        self.arrive_tangent = float(arrive_tangent)
        self.leave_tangent = float(leave_tangent)
        self.interp_mode = interp_mode
        self.tangent_mode = tangent_mode
        self.arrive_weight = float(arrive_weight)
        self.leave_weight = float(leave_weight)
        self.weighted_mode = weighted_mode
        self._handle = 0

    @property
    def handle(self):
        """
        [只读属性]

        获取由 ``Curve`` 分配的关键帧句柄。直接创建的 ``CurveKey`` 在加入曲线前句柄为 ``0`` 。

        :return: 关键帧句柄
        :rtype: int
        """
        return self._handle

    def copy(self):
        """
        创建当前关键帧的拷贝。

        示例
        ----

        >>> key = CurveKey(0.0, 1.0)
        >>> copied = key.copy()
        >>> (copied.time, copied.value)
        (0.0, 1.0)

        -----

        :return: 关键帧拷贝
        :rtype: CurveKey
        """
        key = CurveKey(
            self.time,
            self.value,
            self.arrive_tangent,
            self.leave_tangent,
            self.interp_mode,
            self.tangent_mode,
            self.arrive_weight,
            self.leave_weight,
            self.weighted_mode,
        )
        key._handle = self._handle
        return key

    def __repr__(self):
        return "CurveKey(time=%r, value=%r)" % (self.time, self.value)
