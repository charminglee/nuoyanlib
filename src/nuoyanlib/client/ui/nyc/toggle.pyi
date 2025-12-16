# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from typing import Optional, Callable
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self


__ToggleChangedCallback = Callable[[dict], int]


class NyToggle(NyControl):
    _base_control: SwitchToggleUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        toggle_control: SwitchToggleUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def state(self) -> bool: ...
    @state.setter
    def state(self, val: bool) -> None: ...
    def set_callback(self, func: __ToggleChangedCallback) -> bool: ...
    def remove_callback(self, func: __ToggleChangedCallback) -> bool: ...
    SetCallback = set_callback
    RemoveCallback = remove_callback
    SetToggleState = SwitchToggleUIControl.SetToggleState
    GetToggleState = SwitchToggleUIControl.GetToggleState
