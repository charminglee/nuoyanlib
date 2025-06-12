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
    "NyMiniMap",
]


class NyMiniMap(NyControl):
    """
    | 创建 ``NyMiniMap`` 小地图实例。
    | 兼容ModSDK ``MiniMapUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 小地图所在UI类的实例
    :param MiniMapUIControl mini_map_control: 通过asMiniMap()获取的小地图实例
    """

    _CONTROL_TYPE = ControlType.mini_map

    def __init__(self, screen_node_ex, mini_map_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, mini_map_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











