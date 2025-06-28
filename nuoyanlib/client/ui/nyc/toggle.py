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
    "NyToggle",
]


class NyToggle(NyControl):
    """
    | 创建 ``NyToggle`` 开关实例。
    | 兼容ModSDK ``SwitchToggleUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 开关所在UI类的实例
    :param SwitchToggleUIControl toggle_control: 通过asSwitchToggle()获取的开关实例
    """

    _CONTROL_TYPE = ControlType.toggle

    def __init__(self, screen_node_ex, toggle_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, toggle_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregionik，。

    # region property proxy ===================================================================================

    # endregion











