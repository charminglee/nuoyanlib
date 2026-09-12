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


from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check
from ....core._types._typing import FTuple2


class NyInputPanel(NyControl):
    _base_control: InputPanelUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
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
    set_is_modal = SetIsModal = InputPanelUIControl.SetIsModal
    get_is_modal = GetIsModal = InputPanelUIControl.GetIsModal
    set_is_swallow = SetIsSwallow = InputPanelUIControl.SetIsSwallow
    get_is_swallow = GetIsSwallow = InputPanelUIControl.GetIsSwallow
    set_offset_delta = SetOffsetDelta = InputPanelUIControl.SetOffsetDelta
    get_offset_delta = GetOffsetDelta = InputPanelUIControl.GetOffsetDelta
