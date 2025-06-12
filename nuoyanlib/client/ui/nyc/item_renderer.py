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
    "NyItemRenderer",
]


class NyItemRenderer(NyControl):
    """
    | 创建 ``NyItemRenderer`` 物品渲染器实例。
    | 兼容ModSDK ``ItemRendererUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 物品渲染器所在UI类的实例
    :param ItemRendererUIControl item_renderer_control: 通过asItemRenderer()获取的物品渲染器实例
    """

    _CONTROL_TYPE = ControlType.item_renderer

    def __init__(self, screen_node_ex, item_renderer_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, item_renderer_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











