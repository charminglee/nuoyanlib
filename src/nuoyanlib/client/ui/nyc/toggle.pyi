# -*- coding: utf-8 -*-
#  =================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  =================================================


from typing import Callable, Union
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


__ToggleChangedCallback = Callable[[dict], int]


class NyToggle(NyControl):
    _base_control: SwitchToggleUIControl
    def __init__(
        screen_node_ex: ScreenNodeExtension,
        toggle_control: SwitchToggleUIControl,
        self,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def state(self) -> bool: ...
    @state.setter
    def state(self, val: bool) -> None: ...
    def set_callback(self, func: __ToggleChangedCallback) -> bool: ...
    def remove_callback(self, func: __ToggleChangedCallback) -> bool: ...
    SetToggleState = SwitchToggleUIControl.SetToggleState
    GetToggleState = SwitchToggleUIControl.GetToggleState
