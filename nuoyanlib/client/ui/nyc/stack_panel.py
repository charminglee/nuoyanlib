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
    "NyStackPanel",
]


class NyStackPanel(NyControl):
    """
    | 创建 ``NyStackPanel`` 栈面板实例。
    | 兼容ModSDK ``StackPanelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 栈面板所在UI类的实例
    :param StackPanelUIControl stack_panel_control: 通过asStackPanel()获取的栈面板实例
    """

    _CONTROL_TYPE = ControlType.STACK_PANEL

    def __init__(self, screen_node_ex, stack_panel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, stack_panel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    # endregion











