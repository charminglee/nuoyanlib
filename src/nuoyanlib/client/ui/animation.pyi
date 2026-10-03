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


from typing import Self, Any, Callable, ClassVar, Dict, List, NoReturn, Optional, Sequence, Union, TypeVar, overload, Tuple, Generic
from ...common.mc_math.curve import Curve
from ...core._types._typing import EasingFuncType, T
from ...core._types._checker import args_type_check
from ...core._utils import Singleton, MappingProxy


__StringType = str
__StringT = str
__NumberType = Union[int, float]
__NumberT = TypeVar("__NumberT", bound=__NumberType)
__SequenceType = Union[Tuple[__PropertyTypesBase, ...], List[__PropertyTypesBase]]
__SequenceT = TypeVar("__SequenceT", bound=__SequenceType)
__DictType = Dict[str, __PropertyTypes]
__DictT = TypeVar("__DictT", bound=__DictType)


__PropertyTypesBase = Union[bool, __StringType, __NumberType]
__PropertyTypes = Union[__PropertyTypesBase, __SequenceType, __DictType]
__PropertyT = TypeVar("__PropertyT", bound=__PropertyTypes)


def _copy_value(value: T) -> T: ...
def _check_property(start: __PropertyT, end: __PropertyT, delta: bool) -> None: ...
@overload
def _choice_interp(start: bool, end: bool) -> Callable[[float], bool]: ...
@overload
def _choice_interp(start: __StringT, end: __StringT) -> Callable[[float], __StringT]: ...
@overload
def _choice_interp(start: __NumberT, end: __NumberT) -> Callable[[float], __NumberT]: ...
@overload
def _choice_interp(start: __SequenceT, end: __SequenceT) -> Callable[[float], __SequenceT]: ...
@overload
def _choice_interp(start: __DictT, end: __DictT) -> Callable[[float], __DictT]: ...


class Property(Generic[__PropertyT]):
    __slots__ = (
        'start',
        'end',
        'interp',
        'setter',
        '_delta_start',
        '_delta_end',
        '_fixed_start',
    )
    _delta_start: float
    _delta_end: float
    _fixed_start: bool
    start: __PropertyT
    end: __PropertyT
    interp: Optional[Callable[[float], __PropertyT]]
    setter: Optional[Callable[[str, __PropertyT], Any]]
    @overload
    def __init__(
        self, start: __PropertyT,
        end: __PropertyT,
        *,
        delta_start: bool = False,
        delta_end: bool = False,
        delta: bool = False,
        setter: Optional[Callable[[str, __PropertyT], Any]] = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        end: __PropertyT,
        *,
        delta_start: bool = False,
        delta_end: bool = False,
        delta: bool = False,
        setter: Optional[Callable[[str, __PropertyT], Any]] = None,
    ) -> None: ...
    def _set_start(self, start: __PropertyT) -> None: ...
    def eval_(self, p: float) -> __PropertyT: ...


class AnimationBase(object):
    NONE: ClassVar[int]
    """ 无状态。 """
    IDLE: ClassVar[int]
    """ 动画空闲。 """
    WAITING: ClassVar[int]
    """ 动画正在等待。 """
    PLAYING: ClassVar[int]
    """ 动画正在播放。 """
    PAUSED: ClassVar[int]
    """ 动画暂停。 """
    COMPLETED: ClassVar[int]
    """ 动画完成。 """
    CANCELLED: ClassVar[int]
    """ 动画取消。 """
    ON_START: ClassVar[int]
    """ 动画开始时触发。 """
    ON_UPDATE: ClassVar[int]
    """ 动画更新时触发。 """
    ON_END: ClassVar[int]
    """ 动画结束时触发。 """
    _state: int
    _paused_state: int
    _elapsed: float
    _cycle_index: int
    _progress: float
    duration: float
    """ 动画持续时间，单位为秒。 """
    delay: float
    """ 动画开始前的延迟时间，单位为秒。 """
    repeat: int
    """ 重复次数，设为 ``-1`` 表示无限重复。 """
    is_yoyo: bool
    """ 每次重复时是否反向播放。 """
    next_anim: Optional[AnimationBase]
    """ 下一个动画。 """
    on_start: Optional[Callable[[Self], Any]]
    """
    动画开始时触发的回调函数。
     
    ``on_start(anim:⠀PropertyAnimation)⠀->⠀...``
    
    - ``anim`` -- 当前动画实例。
    """
    on_update: Optional[Callable[[Self], Any]]
    """
    动画更新时触发的回调函数。
     
    ``on_update(anim:⠀PropertyAnimation)⠀->⠀...``

    - ``anim`` -- 当前动画实例。
    """
    on_end: Optional[Callable[[Self], Any]]
    """
    动画结束时触发的回调函数。
     
    ``on_end(anim:⠀PropertyAnimation)⠀->⠀...``

    - ``anim`` -- 当前动画实例。
    """
    def __init__(self, duration: float) -> None: ...
    @property
    def state(self) -> int: ...
    @property
    def elapsed(self) -> float: ...
    @property
    def cycle_index(self) -> float: ...
    @property
    def total_duration(self) -> float: ...
    @property
    def progress(self) -> float: ...
    @progress.setter
    def progress(self, val: float) -> None: ...
    def is_idle(self) -> bool: ...
    def is_waiting(self) -> bool: ...
    def is_playing(self) -> bool: ...
    def is_paused(self) -> bool: ...
    def is_completed(self) -> bool: ...
    def is_cancelled(self) -> bool: ...
    def is_active(self) -> bool: ...
    def is_ended(self) -> bool: ...
    def set_callback(self, func: Callable[[Self], Any], *cb_types: int) -> Self: ...
    def set_delay(self, delay: float) -> Self: ...
    def set_repeat(self, count: int) -> Self: ...
    def set_yoyo(self, yoyo: bool) -> Self: ...
    def set_next(self, next_anim: Optional[AnimationBase]) -> Self: ...
    def start(self, restart: bool = False) -> Self: ...
    def pause(self) -> Self: ...
    def resume(self) -> Self: ...
    def finish(self) -> Self: ...
    def complete(self) -> Self: ...
    def cancel(self, stay: bool = False, call_on_end: bool = True) -> Self: ...
    def _prepare(self) -> None: ...
    def _begin(self) -> None: ...
    def _set_progress(self, progress: float, call_on_update: bool = True) -> None: ...
    def update(self, delta_time: float) -> None: ...


class PropertyAnimation(AnimationBase, Generic[T]):
    _curr_frame: Dict[str, Any]
    targets: T
    """ 执行动画的UI控件实例。 """
    properties: Dict[str, Union[Property, Curve]]
    """ 动画属性字典，与创建动画时传入的属性参数相同。 """
    easing: Optional[EasingFuncType]
    """
    缓动函数。
    
    该函数参数为一个范围为 ``[0,⠀1]`` 的浮点数，返回缓动值用于计算插值。
    """
    @overload
    def __init__(
        self,
        targets: T,
        duration: float,
        easing: EasingFuncType = Curve.Easing.LINEAR,
        /,
        **properties: Union[Property, Curve]
    ) -> None: ...
    @overload
    def __init__(
        self,
        targets: T,
        /,
        **properties: Curve
    ) -> None: ...
    def _prepare(self) -> None: ...
    def _set_progress(self, progress: float, call_on_update: bool = True) -> None: ...
    def update(self, delta_time: float) -> None: ...
    def get_curr_frame(self) -> MappingProxy[str, Any]: ...


class AnimationSequence(AnimationBase, List[PropertyAnimation]):
    def __init__(self, *animations: PropertyAnimation) -> None: ...


class AnimationParallel(AnimationBase, List[AnimationBase]):
    def __init__(self, *animations: AnimationBase) -> None: ...
    @property
    def total_duration(self) -> float: ...
    def set_delay(self, delay: float) -> Self: ...
    def set_repeat(self, count: int) -> Self: ...
    def set_yoyo(self, yoyo: bool) -> NoReturn: ...
    def start(self, restart: bool = False) -> Self: ...
    def pause(self) -> Self: ...
    def resume(self) -> Self: ...
    def finish(self) -> Self: ...
    def complete(self) -> Self: ...
    def cancel(self, stay: bool = False, call_on_end: bool = True) -> Self: ...


class _AnimationManager(Singleton):
    _animations: List[AnimationBase]
    _last_time: float
    def __init__(self) -> None: ...
    def is_active(self) -> bool: ...
    @args_type_check(AnimationBase)
    def add(self, anim: AnimationBase) -> None: ...
    def remove(self, anim: AnimationBase) -> None: ...
    def update(self, delta_time: Optional[float] = ...) -> None: ...
    def clear(self) -> None: ...


_animation_mgr: _AnimationManager