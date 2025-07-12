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
    "NyComboBox",
]


class NyComboBox(NyControl):
    """
    | 创建 ``NyComboBox`` 下拉框实例。
    | 兼容ModSDK ``NeteaseComboBoxUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 下拉框所在UI类的实例
    :param NeteaseComboBoxUIControl combo_box_control: 通过asNeteaseComboBox()获取的下拉框实例
    """

    _CONTROL_TYPE = ControlType.combo_box

    def __init__(self, screen_node_ex, combo_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, combo_box_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region property proxy ============================================================================================

    # endregion











