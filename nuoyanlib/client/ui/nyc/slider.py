# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-22
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
    | 兼容ModSDK ``SliderUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 滑动条所在UI类的实例
    :param SliderUIControl slider_control: 通过asSlider()获取的滑动条实例
    """

    _CONTROL_TYPE = ControlType.SLIDER

    def __init__(self, screen_node_ex, slider_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, slider_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    # endregion











