# -*- coding: utf-8 -*-
#  ================================================
#
#    Copyright (c) 2026 Nuoyan
#
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-10-2
#
#  ================================================


from typing import Any, Callable, List, Optional, Sequence, Tuple, Union
from ...core._types._typing import EasingFuncType


__CurveKeyInput = Union["CurveKey", Tuple[float, float], List[Any]]


class CurveKey(object):
    time: float
    value: float
    arrive_tangent: float
    leave_tangent: float
    interp_mode: Any
    tangent_mode: Any
    def __init__(
        self,
        time: float,
        value: float,
        arrive_tangent: float = 0.0,
        leave_tangent: float = 0.0,
        interp_mode: Any = Curve.InterpMode.CUBIC,
        tangent_mode: Any = Curve.TangentMode.AUTO,
    ) -> None: ...
    def copy(self) -> CurveKey: ...


class Curve(object):
    class Easing:
        LINEAR: EasingFuncType
        """ 线性缓动，变化速度均匀。 """
        SPRING: EasingFuncType
        """ 弹簧缓动，效果通常表现为一个有些反复的波动，随着时间逐渐衰减。 """
        IN_QUAD: EasingFuncType
        """ 二次加速，在开始时慢，随着时间推进加速，二次方增长。 """
        OUT_QUAD: EasingFuncType
        """ 二次减速，在开始时快速，随着时间推移减速，二次方衰减。 """
        IN_OUT_QUAD: EasingFuncType
        """ 二次加减速，先加速然后减速，二次方的组合。 """
        IN_CUBIC: EasingFuncType
        """ 三次加速，在开始时非常慢，然后迅速加速，三次方增长。 """
        OUT_CUBIC: EasingFuncType
        """ 三次减速，在开始时快速，然后减速，三次方衰减。 """
        IN_OUT_CUBIC: EasingFuncType
        """ 三次加减速，先加速然后减速，三次方的组合。 """
        IN_QUART: EasingFuncType
        """ 四次加速，在开始时非常慢，然后迅速加速，四次方增长。 """
        OUT_QUART: EasingFuncType
        """ 四次减速，在开始时非常快，然后逐渐减速，四次方衰减。 """
        IN_OUT_QUART: EasingFuncType
        """ 四次加减速，先加速然后减速，四次方的组合。 """
        IN_QUINT: EasingFuncType
        """ 五次加速，在开始时非常慢，然后急剧加速，五次方增长。 """
        OUT_QUINT: EasingFuncType
        """ 五次减速，在开始时非常快，随后减速，五次方衰减。 """
        IN_OUT_QUINT: EasingFuncType
        """ 五次加减速，先加速然后减速，五次方的组合。 """
        IN_SINE: EasingFuncType
        """ 正弦加速，在开始时慢，随着时间加速，遵循正弦函数的形式。 """
        OUT_SINE: EasingFuncType
        """ 正弦减速，在开始时快，随后减速，遵循正弦函数的形式。 """
        IN_OUT_SINE: EasingFuncType
        """ 正弦加减速，先加速然后减速，遵循正弦函数的形式。 """
        IN_EXPO: EasingFuncType
        """ 指数加速，在开始时非常慢，随后迅速加速，遵循指数函数增长。 """
        OUT_EXPO: EasingFuncType
        """ 指数减速，在开始时非常快，随后减速，遵循指数衰减。 """
        IN_OUT_EXPO: EasingFuncType
        """ 指数加减速，先加速然后减速，遵循指数函数。 """
        IN_CIRC: EasingFuncType
        """ 圆形加速，在开始时较慢，然后加速，遵循圆形函数的效果。 """
        OUT_CIRC: EasingFuncType
        """ 圆形减速，在开始时较快，然后减速，遵循圆形函数的效果。 """
        IN_OUT_CIRC: EasingFuncType
        """ 圆形加减速，先加速然后减速，遵循圆形函数的效果。 """
        IN_BOUNCE: EasingFuncType
        """ 弹跳加速，表现为一种反复弹跳的加速效果。 """
        OUT_BOUNCE: EasingFuncType
        """ 弹跳减速，表现为一种弹跳的减速效果。 """
        IN_OUT_BOUNCE: EasingFuncType
        """ 弹跳加减速，先加速然后减速，表现为弹跳效果。 """
        IN_BACK: EasingFuncType
        """ 回退加速，动画先稍微向后回退，然后加速。 """
        OUT_BACK: EasingFuncType
        """ 回退减速，动画开始时很快，之后回退并逐渐减速。 """
        IN_OUT_BACK: EasingFuncType
        """ 回退加减速，先回退后加速，之后回弹并减速。 """
        IN_ELASTIC: EasingFuncType
        """ 弹性加速，具有弹性拉伸的效果，初期比较慢，然后加速。 """
        OUT_ELASTIC: EasingFuncType
        """ 弹性减速，弹性效果，快速运动然后逐渐回弹。 """
        IN_OUT_ELASTIC: EasingFuncType
        """ 弹性加减速，先加速后减速，表现为弹性效果。 """
    class InterpMode:
        CONSTANT: str
        LINEAR: str
        CUBIC: str
    class TangentMode:
        NONE: str
        AUTO: str
        USER: str
    class Extrapolation:
        CONSTANT: str
        LINEAR: str
        CYCLE: str
        CYCLE_WITH_OFFSET: str
        OSCILLATE: str
    start_val: float
    end_val: float
    total_time: float
    fps: int
    easing: EasingFuncType
    next_curve: Optional[Curve]
    on_start: Optional[Callable[[], Any]]
    on_end: Optional[Callable[[], Any]]
    pre_infinity: str
    post_infinity: str
    _keys: List[CurveKey]
    _key_mode: bool
    _init_tm: float
    _frame: int
    _total_frame: int
    _diff_val: float
    _val: float
    _state: int
    _is_static: bool
    def __init__(
        self,
        start_val: float = 0.0,
        end_val: float = 1.0,
        total_time: float = 1.0,
        fps: int = 0,
        easing: EasingFuncType = ...,
        next: Optional[Curve] = None,
        on_start: Optional[Callable[[], Any]] = None,
        on_end: Optional[Callable[[], Any]] = None,
        keys: Optional[Sequence[__CurveKeyInput]] = None,
        pre_infinity: Any = Extrapolation.CONSTANT,
        post_infinity: Any = Extrapolation.CONSTANT,
    ) -> None: ...
    @classmethod
    def from_keys(
        cls,
        keys: Sequence[__CurveKeyInput],
        pre_infinity: Any = Extrapolation.CONSTANT,
        post_infinity: Any = Extrapolation.CONSTANT,
    ) -> Curve: ...
    @classmethod
    def static(
        cls,
        val: float,
        total_time: float,
        next: Optional[Curve] = None,
        on_start: Optional[Callable[[], Any]] = None,
        on_end: Optional[Callable[[], Any]] = None,
    ) -> Curve: ...
    @property
    def keys(self) -> List[CurveKey]: ...
    @keys.setter
    def keys(self, values: Optional[Sequence[__CurveKeyInput]]) -> None: ...
    @property
    def duration(self) -> float: ...
    @property
    def first_key_time(self) -> float: ...
    @property
    def last_key_time(self) -> float: ...
    @property
    def finished(self) -> bool: ...
    def add_key(
        self,
        key_or_time: __CurveKeyInput,
        value: Any = ...,
        arrive_tangent: float = 0.0,
        leave_tangent: float = 0.0,
        interp_mode: Any = InterpMode.CUBIC,
        tangent_mode: Any = TangentMode.AUTO,
    ) -> CurveKey: ...
    def find_key(self, key_time: float, tolerance: float = 1e-6) -> Optional[CurveKey]: ...
    def update_key(
        self,
        key: Union[CurveKey, int, float],
        time: Any = ...,
        value: Any = ...,
        arrive_tangent: Any = ...,
        leave_tangent: Any = ...,
        interp_mode: Any = ...,
        tangent_mode: Any = ...,
    ) -> Optional[CurveKey]: ...
    def delete_key(self, key: Union[CurveKey, int, float]) -> bool: ...
    def clear(self) -> None: ...
    def eval_(self, at_time: float) -> float: ...
    __call__ = eval_
    def __iter__(self) -> Curve: ...
    def __next__(self) -> float: ...
    next = __next__
    def reset(self) -> None: ...
    def copy(self) -> Curve: ...
    def __copy__(self) -> Curve: ...
    def __deepcopy__(self, memo: Any) -> Curve: ...
