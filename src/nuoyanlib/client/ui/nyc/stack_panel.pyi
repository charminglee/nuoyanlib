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


from typing import Literal
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


class NyStackPanel(NyControl):
    _base_control: StackPanelUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def orientation(self) -> Literal["horizontal", "vertical"]: ...
    @orientation.setter
    def orientation(self, val: Literal["horizontal", "vertical"]) -> None: ...
    set_orientation = SetOrientation = StackPanelUIControl.SetOrientation
    get_orientation = GetOrientation = StackPanelUIControl.GetOrientation
