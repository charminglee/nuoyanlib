# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  ================================================


from typing import Callable, Any, ClassVar, Union
from mod.client.ui.controls.selectionWheelUIControl import SelectionWheelUIControl
from .control import NyControl, InteractableControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....common.enum import WheelCallbackType


__WheelCallbackType = Callable[[], Any]


class NySelectionWheel(InteractableControl, NyControl):
    _base_control: SelectionWheelUIControl
    def __init__(
        screen_node_ex: ScreenNodeExtension,
        selection_wheel_control: SelectionWheelUIControl,
        self,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    def set_callback(
        self,
        func: __WheelCallbackType,
        cb_type: WheelCallbackType = WheelCallbackType.CLICK
    ) -> bool: ...
    def remove_callback(
        self,
        func: __WheelCallbackType,
        cb_type: WheelCallbackType = WheelCallbackType.CLICK,
    ) -> bool: ...
    def _on_click(self) -> None: ...
    def _on_hover(self) -> None: ...
    GetSliceCount = SelectionWheelUIControl.GetSliceCount
    GetCurrentSliceIndex = SelectionWheelUIControl.GetCurrentSliceIndex
    SetCurrentSliceIndex = SelectionWheelUIControl.SetCurrentSliceIndex
    SetTouchUpCallback = SelectionWheelUIControl.SetTouchUpCallback
    SetHoverCallback = SelectionWheelUIControl.SetHoverCallback
