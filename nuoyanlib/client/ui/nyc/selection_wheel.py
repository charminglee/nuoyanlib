# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NySelectionWheel",
]


class NySelectionWheel(NyControl):
    """
    | 创建 ``NySelectionWheel`` 轮盘实例。
    | 兼容ModSDK ``SelectionWheelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 轮盘所在UI类的实例
    :param SelectionWheelUIControl selection_wheel_control: 通过asSelectionWheel()获取的轮盘实例
    """

    _CONTROL_TYPE = ControlType.selection_wheel

    def __init__(self, screen_node_ex, selection_wheel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, selection_wheel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region property proxy ============================================================================================

    # endregion











