# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-13
|
| ====================================================
"""


from typing import Optional, Callable, Any
from mod.client.ui.controls.selectionWheelUIControl import SelectionWheelUIControl
from .control import NyControl, InteractableControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self
from ....utils.enum import WheelCallbackType


__WheelCallbackType = Callable[[], Any]


class NySelectionWheel(InteractableControl, NyControl):
    _base_control: SelectionWheelUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        selection_wheel_control: SelectionWheelUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
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
    SetCallback = set_callback
    RemoveCallback = remove_callback
    GetSliceCount = SelectionWheelUIControl.GetSliceCount
    GetCurrentSliceIndex = SelectionWheelUIControl.GetCurrentSliceIndex
    SetCurrentSliceIndex = SelectionWheelUIControl.SetCurrentSliceIndex
    SetTouchUpCallback = SelectionWheelUIControl.SetTouchUpCallback
    SetHoverCallback = SelectionWheelUIControl.SetHoverCallback
