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
    "NyEditBox",
]


class NyEditBox(NyControl):
    """
    | 创建 ``NyEditBox`` 文本编辑框实例。
    | 兼容ModSDK ``TextEditBoxUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 文本编辑框所在UI类的实例
    :param TextEditBoxUIControl edit_box_control: 通过asTextEditBox()获取的文本编辑框实例
    """

    _CONTROL_TYPE = ControlType.edit_box

    def __init__(self, screen_node_ex, edit_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, edit_box_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











