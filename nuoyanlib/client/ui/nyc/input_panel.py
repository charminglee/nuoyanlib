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
    "NyInputPanel",
]


class NyInputPanel(NyControl):
    """
    | 创建 ``NyInputPanel`` 输入面板实例。
    | 兼容ModSDK ``InputPanelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 输入面板所在UI类的实例
    :param InputPanelUIControl input_panel_control: 通过asInputPanel()获取的输入面板实例
    """

    _CONTROL_TYPE = ControlType.input_panel

    def __init__(self, screen_node_ex, input_panel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, input_panel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region property proxy ============================================================================================

    # endregion











