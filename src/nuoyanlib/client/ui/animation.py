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
import time
from ...core.listener import is_listened, listen_event, unlisten_event
from ...core._utils import args_defaults, Singleton, kwargs_defaults, MappingProxy
from ...core._types._checker import args_type_check
from ...common.mc_math.curve import Curve
from ...common.mc_math.mc_math import lerp, clamp


if bool(0):
    from .nyc.control import NyControl


__all__ = [
    "AnimationBase",
    "Property",
    "PropertyAnimation",
    "AnimationSequence",
    "AnimationParallel",
]


_BOOLEAN_TYPE = (bool,)
_STRING_TYPE = (str, unicode)
_SEQUENCE_TYPE = (list, tuple)
_DICT_TYPE = (dict,)
_NUMBER_TYPES = (int, long, float)
_ALLOWED_TYPES = _NUMBER_TYPES + _STRING_TYPE + _SEQUENCE_TYPE + _DICT_TYPE
_UNSET = object()


def _copy_value(value):
    if isinstance(value, tuple):
        return tuple(_copy_value(item) for item in value)
    if isinstance(value, list):
        return [_copy_value(item) for item in value]
    if isinstance(value, dict):
        return {k: _copy_value(v) for k, v in value.items()}
    if isinstance(value, Curve):
        return value.copy()
    return value


def _check_property(start, end, delta):
    if not isinstance(end, _ALLOWED_TYPES) or (start is not _UNSET and not isinstance(start, _ALLOWED_TYPES)):
        raise TypeError(
            "property value must be a bool, str, number (int/float/long), sequence (list/tuple), dict"
        )
    if (
        delta
        and (
            not isinstance(end, _NUMBER_TYPES)
            or (start is not _UNSET and not isinstance(start, _NUMBER_TYPES))
        )
    ):
        raise TypeError("property value must be a number (int/float/long) when using delta")
    if start is _UNSET:
        return

    if isinstance(start, _BOOLEAN_TYPE) and isinstance(end, _BOOLEAN_TYPE):
        return
    if isinstance(start, _STRING_TYPE) and isinstance(end, _STRING_TYPE):
        return
    if isinstance(start, _NUMBER_TYPES) and isinstance(end, _NUMBER_TYPES):
        return

    if isinstance(start, _SEQUENCE_TYPE) and isinstance(end, _SEQUENCE_TYPE):
        for i, j in zip(start, end):
            _check_property(i, j, delta)
        return
    if isinstance(start, dict) and isinstance(end, dict):
        for k in end:
            if k not in start:
                continue
            _check_property(start[k], end[k], delta)
        return

    raise TypeError(
        "property value types must match; but start is %s, and end is %s"
        % (type(start), type(end))
    )


def _choice_interp(start, end):
    if start == end:
        return lambda t: _copy_value(end)

    if isinstance(end, _BOOLEAN_TYPE) or isinstance(end, _STRING_TYPE):
        return lambda t: start if t < 1.0 else end
    if isinstance(end, _NUMBER_TYPES):
        return lambda t: lerp(start, end, t)

    if isinstance(end, _SEQUENCE_TYPE):
        typ = type(end)
        interp_each_values = [
            _choice_interp(i, j)
            for i, j in zip(start, end)
        ]
        return lambda t: typ(
            interp(t)
            for interp in interp_each_values
        )
    if isinstance(end, _DICT_TYPE):
        typ = type(end)
        interp_each_keys = {
            k: _choice_interp(start[k], end[k])
            for k in end
        }
        return lambda t: typ(
            (k, interp(t))
            for k, interp in interp_each_keys.items()
        )


def _align_values(start, end):
    if isinstance(end, _SEQUENCE_TYPE):
        len_start = len(start)
        len_end = len(end)
        if len_start > len_end:
            start = start[:len_end]
        elif len_end > len_start:
            end = end[:len_start]
    elif isinstance(end, _DICT_TYPE):
        for k in start.keys():
            if k not in end:
                del start[k]
        for k in end.keys():
            if k not in start:
                del end[k]
    return start, end


class Property(object):
    __slots__ = (
        'start',
        'end',
        'interp',
        'setter',
        '_delta_start',
        '_delta_end',
        '_fixed_start',
    )

    @kwargs_defaults(
        delta_start=False,
        delta_end=False,
        delta=None,
        setter=None,
    )
    def __init__(self, start, end=_UNSET, **kwargs):
        delta = kwargs['delta']
        delta_start = kwargs['delta_start']
        delta_end = kwargs['delta_end']
        if delta is not None:
            delta_start = delta
            delta_end = delta
        use_delta = delta_start or delta_end
        if end is _UNSET:
            _check_property(_UNSET, start, use_delta) # noqa
            self.start = _UNSET # noqa
            self.end = start
            self.interp = None
            self._delta_start = 0
            self._delta_end = start if delta_end else 0
            self._fixed_start = False
        else:
            _check_property(start, end, use_delta)
            start, end = _align_values(start, end)
            self.start = start
            self.end = end
            self.interp = _choice_interp(start, end)
            self._delta_start = start if delta_start else 0
            self._delta_end = end if delta_end else 0
            self._fixed_start = True
        self.setter = kwargs['setter']

    def _set_start(self, start):
        _check_property(start, self.end, self._delta_start or self._delta_end)
        if not self._fixed_start:
            self.start = start
        elif self._delta_start:
            self.start = start + self._delta_start
        if self._delta_end:
            self.end = start + self._delta_end
        self.start, self.end = _align_values(self.start, self.end)
        self.interp = _choice_interp(self.start, self.end)

    def eval_(self, t):
        if not self.interp:
            raise ValueError("'interp' not set")
        return self.interp(t)
    
    
class AnimationBase(object):
    NONE = -1
    IDLE = 0
    WAITING = 1
    PLAYING = 2
    PAUSED = 3
    COMPLETED = 4
    CANCELLED = 5

    ON_START = 0
    ON_UPDATE = 1
    ON_END = 2
    
    def __init__(self, duration):
        if duration == 0.0:
            raise ValueError("'duration' cannot be zero")
        self._state = self.IDLE
        self._paused_state = self.NONE
        self._elapsed = 0.0
        self._cycle_index = 0
        self._progress = 0.0
        self.duration = duration
        self.delay = 0.0
        self.repeat = 0
        self.is_yoyo = False
        self.next_anim = None
        self.on_start = None
        self.on_update = None
        self.on_end = None

    @property
    def state(self):
        """
        [只读属性]

        当前动画状态。

        :rtype: int
        """
        return self._state

    @property
    def elapsed(self):
        """
        [只读属性]

        动画已经过的时间，包含延迟时间。

        :rtype: float
        """
        return self._elapsed

    @property
    def cycle_index(self):
        """
        [只读属性]

        当前动画周期的索引。

        :rtype: float
        """
        return self._cycle_index

    @property
    def total_duration(self):
        """
        [只读属性]

        动画的总持续时间，包含延迟时间和重复时间。若动画为无限重复，返回 ``-1.0`` 。

        :rtype: float
        """
        if self.repeat < 0:
            return -1.0
        return self.delay + self.duration * (self.repeat + 1)

    @property
    def progress(self):
        """
        [可读写属性]

        当前动画周期的线性进度。

        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, val):
        """
        [可读写属性]

        当前动画周期的线性进度。

        :type val: float
        """
        if val >= 1.0:
            self.complete()
        else:
            self._set_progress(val)

    def is_idle(self):
        """
        判断动画是否空闲。

        -----

        :return: 是否空闲
        :rtype: bool
        """
        return self._state == self.IDLE

    def is_waiting(self):
        """
        判断动画是否正在等待延迟结束。

        -----

        :return: 是否正在等待
        :rtype: bool
        """
        return self._state == self.WAITING

    def is_playing(self):
        """
        判断动画是否正在播放。

        -----

        :return: 是否正在播放
        :rtype: bool
        """
        return self._state == self.PLAYING

    def is_paused(self):
        """
        判断动画是否暂停。

        -----

        :return: 是否暂停
        :rtype: bool
        """
        return self._state == self.PAUSED

    def is_completed(self):
        """
        判断动画是否正常完成。

        -----

        :return: 是否正常完成
        :rtype: bool
        """
        return self._state == self.COMPLETED

    def is_cancelled(self):
        """
        判断动画是否已取消。

        -----

        :return: 是否已取消
        :rtype: bool
        """
        return self._state == self.CANCELLED

    def is_active(self):
        """
        判断动画是否活跃（包括等待、播放和暂停状态）。

        -----

        :return: 是否处于等待、播放或暂停状态
        :rtype: bool
        """
        return self._state in (self.WAITING, self.PLAYING, self.PAUSED)

    def is_ended(self):
        """
        判断动画是否已结束（包括正常完成和取消状态）。

        -----

        :return: 是否已结束
        :rtype: bool
        """
        return self._state in (self.COMPLETED, self.CANCELLED)

    def set_callback(self, func, *cb_types):
        """
        设置动画的回调函数。

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 PropertyAnimation 枚举值；可同时传入多个类型

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        for t in cb_types:
            if t == self.ON_START:
                self.on_start = func
            elif t == self.ON_UPDATE:
                self.on_update = func
            elif t == self.ON_END:
                self.on_end = func
        return self

    def set_delay(self, delay):
        """
        设置动画开始前的延迟时间，单位为秒。

        -----

        :param float delay: 延迟时间

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        self.delay = delay
        return self

    def set_repeat(self, count):
        """
        设置动画重复次数，设为 ``-1`` 表示无限重复。

        -----

        :param int count: 重复次数

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        self.repeat = count
        return self

    def set_yoyo(self, yoyo):
        """
        设置每次动画重复时是否反向播放。

        -----

        :param bool yoyo: 是否反向播放

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        self.is_yoyo = yoyo
        return self

    def set_next(self, next_anim):
        """
        设置下一个动画。

        当前动画播放完成后自动启动下一个动画。

        -----

        :param AnimationBase next_anim: 下一个动画实例

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        self.next_anim = next_anim
        return self

    def start(self, restart=False, _add_to_mgr=True):
        """
        开始播放动画。

        说明
        ----

        动画处于非活跃状态（空闲、完成、取消）时再次调用即可重新播放。

        -----

        :param bool restart: 若当前动画正在播放，是否从头开始播放；默认为 False

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if self.is_active() and not restart:
            return self
        self._prepare()
        if _add_to_mgr:
            _animation_mgr.add(self)
        return self

    def pause(self):
        """
        暂停动画。

        -----

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if not self.is_waiting() and not self.is_playing():
            return
        self._paused_state = self._state
        self._state = self.PAUSED
        return self

    def resume(self):
        """
        恢复已暂停的动画。

        -----

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if not self.is_paused():
            return
        self._state = self._paused_state
        self._paused_state = self.NONE
        return self

    def finish(self):
        """
        立即完成动画，跳过剩余延迟和重复周期。

        -----

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if not self.is_active():
            return self
        self._state = self.COMPLETED
        self._set_progress(1.0)
        if self.repeat >= 0:
            self._cycle_index = self.repeat + 1
            self._elapsed = self.total_duration
        if self.on_end:
            self.on_end(self)
        if self.next_anim:
            self.next_anim.start()
        return self

    def complete(self):
        """
        立即完成当前周期。

        -----

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if not self.is_active():
            return self
        if 0 <= self.repeat <= self._cycle_index:
            self.finish()
            return self
        self._set_progress(1.0)
        self._cycle_index += 1
        self._elapsed = self.delay + self.duration * self._cycle_index
        return self

    def cancel(self, stay=False, call_on_end=True):
        """
        取消动画。

        -----

        :param bool stay: 动画是否停留在当前帧；若设为 True ，取消时所有属性将停留在当前状态，否则恢复初始状态；默认为 False
        :param bool call_on_end: 是否触发动画结束回调；默认为 True

        :return: 当前动画实例
        :rtype: PropertyAnimation
        """
        if not self.is_active():
            return self
        self._state = self.CANCELLED
        if not stay:
            self._elapsed = 0.0
            self._set_progress(0.0, False)
        if call_on_end and self.on_end:
            self.on_end(self)
        return self

    def _prepare(self):
        self._state = self.WAITING
        self._paused_state = self.NONE
        self._elapsed = 0.0
        self._progress = 0.0
        self._cycle_index = 0
        if self.delay <= 0.0:
            self._begin()

    def _begin(self):
        if self._state != self.WAITING:
            return
        self._state = self.PLAYING
        if self.on_start:
            self.on_start(self)

    def _set_progress(self, progress, call_on_update=True):
        self._progress = clamp(progress, 0.0, 1.0)
        if call_on_update and self.on_update:
            self.on_update(self)

    def update(self, delta_time):
        raise NotImplementedError


class PropertyAnimation(AnimationBase):
    """
    UI属性动画类。

    说明
    ----

    构造 PropertyAnimation 对象
    ===========================

    构造函数：

    - ``PropertyAnimation(targets,⠀duration,⠀easing=Curve.Easing.LINEAR,⠀/,⠀**properties)``
    - ``PropertyAnimation(targets,⠀/,⠀**properties)``

    ``/`` 表示前面的参数只能以位置参数的形式传入，不得使用关键字参数。

    构造动画属性
    ============

    使用起始值和目标值
    ~~~~~~~~~~~~~~~~

    每个动画属性使用 ``Property`` 对象表示，其两个参数分别为起始值和目标值。
    支持的类型包括：``bool`` 、 ``str`` 、数字（ ``int`` / ``float`` / ``long`` ）、序列（ ``list`` / ``tuple`` ）、 ``dict`` 。

    下面将构造一个时长 ``1`` 秒，不透明度 ``0`` -> ``1`` ， XY 尺寸 ``(30,⠀30)`` -> ``(100,⠀100)`` 的动画，使用的缓动函数为正弦加速。

    >>> from <scripts_root>.nuoyanlib.client import PropertyAnimation, Property, Curve
    >>> PropertyAnimation(
    ...     control, 1, Curve.Easing.IN_SINE,
    ...     alpha=Property(0, 1),
    ...     size=Property((30, 30), (100, 100)),
    ... )

    注意，当属性类型为 ``bool`` 或 ``str`` 时，将不会进行插值，而是在动画开始/结束时直接设置对应的值。
    例如 ``visible=Property(True,⠀False)`` 将在动画开始时显示控件，动画结束时隐藏控件。

    只使用目标值
    ~~~~~~~~~~~~

    当 ``Property`` 仅传入一个参数时，该参数表示目标值，动画开始时将以属性此刻的值作为起始值。

    假设控件在动画开始时不透明度为 ``0`` ， XY 尺寸为 ``(30,⠀30)`` ，则下方示例与上一个示例等价。

    >>> PropertyAnimation(
    ...     control, 1, Curve.Easing.IN_SINE,
    ...     alpha=Property(1),
    ...     size=Property((100, 100)),
    ... )

    使用 Curve
    ~~~~~~~~~~

    使用 ``Curve`` 时，可省略 ``PropertyAnimation`` 的 ``duration`` 和 ``easing`` 参数，此时所有动画参数将以 ``Curve`` 中设置的为准。

    >>> PropertyAnimation(
    ...     control,
    ...     alpha=Curve(0, 1, 1, easing=Curve.Easing.OUT_QUART),
    ...     size=Curve((30, 30), (100, 100), 1, easing=Curve.Easing.OUT_SINE),
    ... )

    ``Curve`` 可以对属性进行更精细的插值和控制。使用 ``Curve`` 后，动画的总时长取所有 ``Curve`` 时长中的最大值。
    更多信息详见 ``Curve`` 的文档。

    注意：不能将 ``Property`` 和 ``Curve`` 混合使用。

    动画控制
    ========

    - ``.set_callback()`` -- 设置动画的回调函数。
    - ``.set_delay()`` -- 设置动画开始前的延迟时间，单位为秒。
    - ``.set_repeat()`` -- 设置动画重复次数，设为 ``-1`` 表示无限重复。
    - ``.set_yoyo()`` -- 设置每次动画重复时是否反向播放。
    - ``.start()`` -- 开始播放动画。
    - ``.pause()`` -- 暂停动画。
    - ``.resume()`` -- 恢复已暂停的动画。
    - ``.finish()`` -- 立即完成动画，跳过剩余延迟和重复周期。
    - ``.complete()`` -- 立即完成当前周期。
    - ``.cancel()`` -- 取消动画。

    示例
    ----

    >>> control = nyl.NyControl(self, "/panel")
    >>> nyl.PropertyAnimation(
    ...     control, 1, Curve.Easing.IN_SINE,
    ...     alpha=Property(0, 1),
    ...     size=Property((30, 30), (100, 100)),
    ... ).start()

    -----

    :param NyControl targets: [仅位置参数] 要执行动画的UI控件 NyControl 实例或实例列表
    :param float duration: [仅位置参数] 动画持续时间，单位为秒；属性全部使用 Curve 时可省略
    :param function easing: [仅位置参数] 缓动函数；该函数参数为一个范围为 [0, 1] 的浮点数，返回缓动值用于计算插值；默认为 Curve.Easing.LINEAR ；属性全部使用 Curve 时可省略
    :param Any properties: 通过关键字参数传入属性名称以及属性起始值和目标值，详见说明和示例
    """

    @args_defaults(
        ('targets', None),
        ('duration', None),
        ('easing', Curve.Easing.LINEAR),
    )
    def __init__(self, *args, **properties):
        targets = args[0]
        if not isinstance(targets, _SEQUENCE_TYPE):
            targets = [targets]
        is_curve = False
        for i, (name, prop) in enumerate(properties.items()):
            if i == 0:
                is_curve = isinstance(prop, Curve)
            else:
                if (is_curve and not isinstance(prop, Curve)) or (not is_curve and not isinstance(prop, Property)):
                    raise TypeError("properties must all be of type Property or all be of type Curve")
            for tar in targets:
                if not hasattr(tar, name):
                    raise AttributeError(
                        "'%s' object has no attribute '%s'"
                        % (type(tar).__name__, name)
                    )

        if is_curve:
            duration = max(curve.duration for curve in properties.values())
            easing = None
        else:
            duration = args[1]
            if duration is None:
                raise ValueError("missing parameter 'duration'")
            easing = args[2]

        AnimationBase.__init__(self, duration)
        self._curr_frame = {k: None for k in properties}
        self.targets = targets
        self.easing = easing
        self.properties = properties

    def _prepare(self):
        for name, prop in self.properties.items():
            if isinstance(prop, Curve):
                continue
            if not prop._fixed_start or prop._delta_start or prop._delta_end:
                start = getattr(self.targets[0], name)
                prop._set_start(start)
        AnimationBase._prepare(self)

    def _set_progress(self, progress, call_on_update=True):
        if self.is_yoyo and self._cycle_index % 2:
            prop_progress = 1.0 - progress
        else:
            prop_progress = progress
        eased_progress = self.easing(prop_progress) if self.easing else prop_progress
        for name, prop in self.properties.items():
            value = prop.eval_(eased_progress)
            for tar in self.targets:
                if isinstance(prop, Property) and prop.setter:
                    prop.setter(name, value)
                else:
                    tar.__setattr__(name, value)
            self._curr_frame[name] = value
        AnimationBase._set_progress(self, progress, call_on_update)

    def update(self, delta_time):
        if self._state == self.PAUSED:
            return
        if self._state not in (self.WAITING, self.PLAYING):
            return

        self._elapsed += delta_time
        if self._state == self.WAITING:
            if self._elapsed < self.delay:
                return
            self._begin()
            if self._state != self.PLAYING:
                return

        progress_delta = delta_time / self.duration
        if self._progress >= 1.0:
            progress = progress_delta
        else:
            progress = self._progress + progress_delta
        if progress >= 1.0:
            self.complete()
        else:
            self._set_progress(progress, True)

    def get_curr_frame(self):
        """
        获取当前动画帧的属性值字典。

        -----

        :return: 当前动画帧的属性值字典，键为属性名，值为属性值，不可修改
        :rtype: dict
        """
        return MappingProxy(self._curr_frame)


# todo
class AnimationSequence(AnimationBase, list):
    def __init__(self, *animations):
        list.__init__(self, animations)
        duration = sum(anim.duration for anim in animations)
        AnimationBase.__init__(self, duration)

    def start(self):
        AnimationBase.start(self)
        return self

    def pause(self):
        AnimationBase.pause(self)
        return self

    def resume(self):
        AnimationBase.resume(self)
        return self

    def finish(self):
        AnimationBase.finish(self)
        return self

    def cancel(self, stay=False, call_on_end=True):
        AnimationBase.cancel(self, stay, call_on_end)
        return self


class AnimationParallel(AnimationBase, list):
    def __init__(self, *animations):
        list.__init__(self, animations)
        duration = 0.0
        for anim in animations:
            anim.delay = 0
            total_duration = anim.total_duration
            if total_duration < 0:
                duration = -1.0
                break
            if total_duration > duration:
                duration = total_duration
        AnimationBase.__init__(self, duration)

    @property
    def total_duration(self):
        if self.duration < 0 or self.repeat < 0:
            return -1.0
        return self.delay + self.duration * (self.repeat + 1)

    def set_delay(self, delay):
        for anim in self:
            anim.set_delay(delay)
        return AnimationBase.set_delay(self, delay)

    def set_repeat(self, count):
        for anim in self:
            anim.set_repeat(count)
        return AnimationBase.set_repeat(self, count)

    def set_yoyo(self, yoyo):
        raise TypeError("AnimationParallel object does not support '.set_yoyo()'")

    def start(self, restart=False, _add_to_mgr=True):
        if self.is_active() and not restart:
            return self
        for anim in self:
            anim.start(restart, False) # noqa
        return AnimationBase.start(self, restart, _add_to_mgr) # noqa

    def pause(self):
        if not self.is_waiting() and not self.is_playing():
            return
        for anim in self:
            anim.pause()
        return AnimationBase.pause(self)

    def resume(self):
        if not self.is_paused():
            return
        for anim in self:
            anim.resume()
        return AnimationBase.resume(self)

    def finish(self):
        if not self.is_active():
            return self
        for anim in self:
            anim.finish()
        return AnimationBase.finish(self)

    def complete(self):
        if not self.is_active():
            return self
        for anim in self:
            anim.complete()
        if 0 <= self.repeat <= self._cycle_index:
            AnimationBase.finish(self)
            return self
        AnimationBase._set_progress(self, 1.0)
        self._cycle_index += 1
        self._elapsed = self.delay + self.duration * self._cycle_index
        return self

    def cancel(self, stay=False, call_on_end=True):
        if not self.is_active():
            return self
        for anim in self:
            anim.cancel(stay, call_on_end)
        return AnimationBase.cancel(self, stay, call_on_end)

    def update(self, delta_time):
        state = self._state
        if state == self.PAUSED:
            return
        if state != self.WAITING and state != self.PLAYING:
            return

        for anim in self:
            if anim.is_active():
                anim.update(delta_time)

        self._elapsed += delta_time
        if self._state == self.WAITING:
            if self._elapsed < self.delay:
                return
            AnimationBase._begin(self)
            if self._state != self.PLAYING:
                return

        progress_delta = delta_time / self.duration
        if self._progress >= 1.0:
            progress = progress_delta
        else:
            progress = self._progress + progress_delta
        if progress >= 1.0:
            AnimationBase.complete(self)
        else:
            AnimationBase._set_progress(self, progress)


class _AnimationManager(Singleton):
    def __init__(self):
        self._animations = []
        self._last_time = None

    def GameRenderTickEvent(self, args):
        if self._animations:
            self.update()

    def is_active(self):
        return bool(self._animations)

    @args_type_check((PropertyAnimation, AnimationParallel))
    def add(self, anim):
        if not self._animations:
            self._last_time = None
        if anim.is_active() and anim not in self._animations:
            self._animations.append(anim)
            if not is_listened(self.GameRenderTickEvent):
                listen_event(self.GameRenderTickEvent)

    def remove(self, anim):
        if anim in self._animations:
            self._animations.remove(anim)
        if not self._animations:
            self._last_time = None
            unlisten_event(self.GameRenderTickEvent)

    def update(self, delta_time=None):
        if delta_time is None:
            now = time.time()
            if self._last_time is None:
                delta_time = 0.0
            else:
                delta_time = max(0.0, now - self._last_time)
            self._last_time = now
        else:
            self._last_time = time.time()

        for anim in self._animations:
            if anim.is_active():
                anim.update(delta_time)

        for i in range(len(self._animations) - 1, -1, -1):
            anim = self._animations[i]
            if not anim.is_active():
                self.remove(anim)

    def clear(self):
        for anim in self._animations:
            anim.cancel(call_on_end=False)
        self._animations = []
        self._last_time = None
        unlisten_event(self.GameRenderTickEvent)


_animation_mgr = _AnimationManager()
