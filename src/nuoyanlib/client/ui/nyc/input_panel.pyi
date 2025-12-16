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


from typing import Optional
from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self, FTuple2


class NyInputPanel(NyControl):
    _base_control: InputPanelUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        input_panel_control: InputPanelUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def is_modal(self) -> bool: ...
    @is_modal.setter
    def is_modal(self, val: bool) -> None: ...
    @property
    def is_swallow(self) -> bool: ...
    @is_swallow.setter
    def is_swallow(self, val: bool) -> None: ...
    @property
    def offset_delta(self) -> FTuple2: ...
    @offset_delta.setter
    def offset_delta(self, val: FTuple2) -> None: ...
    SetIsModal = InputPanelUIControl.SetIsModal
    GetIsModal = InputPanelUIControl.GetIsModal
    SetIsSwallow = InputPanelUIControl.SetIsSwallow
    GetIsSwallow = InputPanelUIControl.GetIsSwallow
    SetOffsetDelta = InputPanelUIControl.SetOffsetDelta
    GetOffsetDelta = InputPanelUIControl.GetOffsetDelta
