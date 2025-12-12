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


if 0:
    from mod.client.ui.controls.sliderUIControl import SliderUIControl
    from ..screen_node import ScreenNodeExtension


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NySlider",
]


class NySlider(NyControl):
    """
    滑动条控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 滑动条所在UI类的实例（需继承ScreenNodeExtension）
    :param SliderUIControl slider_control: 通过asSlider()等方式获取的SliderUIControl实例
    """

    CONTROL_TYPE = ControlType.SLIDER

    def __init__(self, screen_node_ex, slider_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, slider_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def value(self):
        """
        [可读写属性]

        滑动条的值。

        :rtype: float
        """
        return self._base_control.GetSliderValue()

    @value.setter
    def value(self, val):
        """
        [可读写属性]

        滑动条的值。

        :type val: float
        """
        self._base_control.SetSliderValue(val)

    # endregion











