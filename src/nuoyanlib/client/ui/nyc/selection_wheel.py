# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from ....utils.enum import ControlType, WheelCallbackType
from .control import NyControl, InteractableControl


__all__ = [
    "NySelectionWheel",
]


class NySelectionWheel(InteractableControl, NyControl):
    """
    轮盘控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 轮盘所在UI类的实例（需继承ScreenNodeExtension）
    :param SelectionWheelUIControl selection_wheel_control: 通过asSelectionWheel()等方式获取的SelectionWheelUIControl实例
    """

    CONTROL_TYPE = ControlType.SELECTION_WHEEL
    CALLBACK_TYPE = WheelCallbackType

    def __init__(self, screen_node_ex, selection_wheel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, selection_wheel_control)
        InteractableControl.__init__(
            self,
            {
                WheelCallbackType.CLICK: (selection_wheel_control.SetTouchUpCallback, self._on_click),
                WheelCallbackType.HOVER: (selection_wheel_control.SetHoverCallback, self._on_hover),
            },
        )

    def __destroy__(self):
        NyControl.__destroy__(self)
        InteractableControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def slice_count(self):
        """
        [只读属性]

        轮盘切片数量。

        :rtype: int
        """
        return self._base_control.GetSliceCount()

    @property
    def curr_slice_index(self):
        """
        [可读写属性]

        轮盘当前选择的切片的索引。

        :rtype: int
        """
        return self._base_control.GetCurrentSliceIndex()

    @curr_slice_index.setter
    def curr_slice_index(self, val):
        """
        [可读写属性]

        轮盘当前选择的切片的索引。

        :type val: int
        """
        self._base_control.SetCurrentSliceIndex(val)

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, cb_type=WheelCallbackType.CLICK):
        """
        设置轮盘回调函数。

        支持同时设置多个同类型的回调，按设置顺序依次触发。

        注意：调用本方法后请勿再调用ModSDK的设置轮盘回调的接口（如 ``.SetTouchUpCallback()``），
        否则所有通过本方法设置的回调函数将无效。

        -----

        :param function func: 回调函数
        :param str cb_type: 回调类型，请使用WheelCallbackType枚举值，默认为WheelCallbackType.CLICK

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.set_callback(self, func, cb_type)

    def remove_callback(self, func, cb_type=WheelCallbackType.CLICK):
        """
        移除通过 ``.set_callback()`` 设置的下拉框回调函数。

        -----

        :param function func: 回调函数
        :param str cb_type: 回调类型，请使用WheelCallbackType枚举值，默认为WheelCallbackType.CLICK

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.remove_callback(self, func, cb_type)

    _on_click = lambda self, *args: self._exec_callbacks(WheelCallbackType.CLICK, *args)
    _on_hover = lambda self, *args: self._exec_callbacks(WheelCallbackType.HOVER, *args)

    SetCallback = set_callback
    RemoveCallback = remove_callback

    # endregion










