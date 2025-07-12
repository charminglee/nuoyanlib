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
    "NyScrollView",
]


class NyScrollView(NyControl):
    """
    | 创建 ``NyScrollView`` 滚动视图实例。
    | 兼容ModSDK ``ScrollViewUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 滚动视图所在UI类的实例
    :param ScrollViewUIControl scroll_view_control: 通过asScrollView()获取的滚动视图实例
    """

    _CONTROL_TYPE = ControlType.scroll_view

    def __init__(self, screen_node_ex, scroll_view_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, scroll_view_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region property proxy ============================================================================================

    # endregion











