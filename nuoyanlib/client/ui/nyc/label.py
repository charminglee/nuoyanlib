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


from ..ui_utils import ControlType
from .control import NyControl


__all__ = [
    "NyLabel",
]


class NyLabel(NyControl):
    """
    | 创建 ``NyLabel`` 文本实例。
    | 兼容ModSDK ``LabelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 文本所在UI类的实例
    :param LabelUIControl label_control: 通过asLabel()获取的文本实例
    """

    _CONTROL_TYPE = ControlType.label

    def __init__(self, screen_node_ex, label_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, label_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











