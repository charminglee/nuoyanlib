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


from typing import Literal, Union
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NyStackPanel(NyControl):
    _base_control: StackPanelUIControl
    def __init__(
        screen_node_ex: ScreenNodeExtension,
        stack_panel_control: StackPanelUIControl,
        self,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def orientation(self) -> Literal["horizontal", "vertical"]: ...
    @orientation.setter
    def orientation(self, val: Literal["horizontal", "vertical"]) -> None: ...
    SetOrientation = StackPanelUIControl.SetOrientation
    GetOrientation = StackPanelUIControl.GetOrientation
