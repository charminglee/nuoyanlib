# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-13
|
| ====================================================
"""


if 0:
    from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
    from ..screen_node import ScreenNodeExtension


from ....utils.enum import ControlType
from ....core import error
from .control import NyControl


__all__ = [
    "NyMiniMap",
]


class NyMiniMap(NyControl):
    """
    小地图控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 小地图所在UI类的实例（需继承ScreenNodeExtension）
    :param MiniMapUIControl mini_map_control: 通过asMiniMap()等方式获取的MiniMapUIControl实例
    """

    CONTROL_TYPE = ControlType.MINI_MAP

    def __init__(self, screen_node_ex, mini_map_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, mini_map_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def highest_y(self):
        """
        [只写属性]

        设置绘制地图的最大高度。

        :rtype: None
        """
        raise error.GetPropertyError("texture")

    @highest_y.setter
    def highest_y(self, val):
        """
        [只写属性]

        设置绘制地图的最大高度。

        :type val: int
        """
        self._base_control.SetHighestY(int(val))

    # endregion











