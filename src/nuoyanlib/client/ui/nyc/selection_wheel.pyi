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


from typing import Callable, Any, ClassVar
from mod.client.ui.controls.selectionWheelUIControl import SelectionWheelUIControl
from .control import NyControl, InteractableControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


__WheelCallbackType = Callable[[], Any]


class NySelectionWheel(InteractableControl, NyControl):
    CLICK: ClassVar[int]
    """ 点击轮盘切片时触发。 """
    HOVER: ClassVar[int]
    """ 选择轮盘切片时触发。 """
    _base_control: SelectionWheelUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    def set_callback(self, func: __WheelCallbackType, *cb_types: int) -> None: ...
    def remove_callback(self, func: __WheelCallbackType, *cb_types: int) -> None: ...
    def _on_click(self) -> None: ...
    def _on_hover(self) -> None: ...
    get_slice_count = GetSliceCount = SelectionWheelUIControl.GetSliceCount
    get_current_slice_index = GetCurrentSliceIndex = SelectionWheelUIControl.GetCurrentSliceIndex
    set_current_slice_index = SetCurrentSliceIndex = SelectionWheelUIControl.SetCurrentSliceIndex
    set_touch_up_callback = SetTouchUpCallback = SelectionWheelUIControl.SetTouchUpCallback
    set_hover_callback = SetHoverCallback = SelectionWheelUIControl.SetHoverCallback
