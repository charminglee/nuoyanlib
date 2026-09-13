# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


from typing import Callable, ClassVar, Union
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from ....core._types._checker import args_type_check
from ....core._types._typing import NyScreenBaseT
from .control import NyControl


__ToggleChangedCallback = Callable[[dict], int]


class NyToggle(NyControl[NyScreenBaseT]):
    CHANGED: ClassVar[int]
    """ 开关状态变化时触发。 """
    _base_control: SwitchToggleUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBaseT,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl[NyScreenBaseT]: ...
    __div__ = __truediv__
    @property
    def state(self) -> bool: ...
    @state.setter
    def state(self, val: Union[bool, int]) -> None: ...
    def set_callback(self, func: __ToggleChangedCallback) -> None: ...
    def remove_callback(self, func: __ToggleChangedCallback) -> None: ...
    set_toggle_state = SetToggleState = SwitchToggleUIControl.SetToggleState
    get_toggle_state = GetToggleState = SwitchToggleUIControl.GetToggleState
