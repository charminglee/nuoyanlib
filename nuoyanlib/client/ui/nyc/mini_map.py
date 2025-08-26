# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-27
|
| ==============================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyMiniMap",
]


class NyMiniMap(NyControl):
    """
    | 创建 ``NyMiniMap`` 小地图实例。
    | 兼容ModSDK ``MiniMapUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 小地图所在UI类的实例（需继承ScreenNodeExtension）
    :param MiniMapUIControl mini_map_control: 通过asMiniMap()等方式获取的MiniMapUIControl实例
    """

    _CONTROL_TYPE = ControlType.MINI_MAP

    def __init__(self, screen_node_ex, mini_map_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, mini_map_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    # endregion











