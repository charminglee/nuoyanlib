# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from typing import Optional, Literal
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self


class NyStackPanel(NyControl):
    _base_control: StackPanelUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        stack_panel_control: StackPanelUIControl,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def orientation(self) -> Literal["horizontal", "vertical"]: ...
    @orientation.setter
    def orientation(self, val: Literal["horizontal", "vertical"]) -> None: ...
    SetOrientation = StackPanelUIControl.SetOrientation
    GetOrientation = StackPanelUIControl.GetOrientation
