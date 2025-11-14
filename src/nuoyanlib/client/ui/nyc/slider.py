# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-11-04
|
| ==============================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NySlider",
]


class NySlider(NyControl):
    """
    | 创建 ``NySlider`` 滑动条实例。

    -----

    :param ScreenNodeExtension screen_node_ex: 滑动条所在UI类的实例（需继承ScreenNodeExtension）
    :param SliderUIControl slider_control: 通过asSlider()等方式获取的SliderUIControl实例
    """

    _CONTROL_TYPE = ControlType.SLIDER

    def __init__(self, screen_node_ex, slider_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, slider_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    @property
    def value(self):
        """
        [可读写属性]

        | 滑动条的值。

        :rtype: float
        """
        return self.base_control.GetSliderValue()

    @value.setter
    def value(self, val):
        """
        [可读写属性]

        | 滑动条的值。

        :type val: float
        """
        self.base_control.SetSliderValue(val)

    # endregion











