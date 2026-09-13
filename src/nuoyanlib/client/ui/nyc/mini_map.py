# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core import error
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyMiniMap",
]


class NyMiniMap(NyControl):
    """
    小地图控件类。

    示例
    ----

    >>> self.mini_map = nyl.NyMiniMap(self, "/panel/mini_map")
    >>> self.mini_map.highest_y = 128

    参见
    ----

    - ``NyControl.to_mini_map()`` -- 将通用控件实例转换为小地图控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该小地图控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.MINI_MAP

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def highest_y(self):
        """
        [只写属性]

        设置绘制地图的最大高度。

        :rtype: None
        """
        raise error.GetPropertyError("highest_y")

    @highest_y.setter
    def highest_y(self, val):
        """
        [只写属性]

        设置绘制地图的最大高度。

        :type val: int
        """
        self._base_control.SetHighestY(val)

    # endregion

    # region Compatibility =============================================================================================

    zoom_in                   = ZoomIn                 = lambda s, *a, **k: s._base_control.ZoomIn(*a, **k)
    zoom_out                  = ZoomOut                = lambda s, *a, **k: s._base_control.ZoomOut(*a, **k)
    zoom_reset                = ZoomReset              = lambda s, *a, **k: s._base_control.ZoomReset(*a, **k)
    set_highest_y             = SetHighestY            = lambda s, *a, **k: s._base_control.SetHighestY(*a, **k)
    add_entity_marker         = AddEntityMarker        = lambda s, *a, **k: s._base_control.AddEntityMarker(*a, **k)
    add_entity_text_marker    = AddEntityTextMarker    = lambda s, *a, **k: s._base_control.AddEntityTextMarker(*a, **k)
    add_static_marker         = AddStaticMarker        = lambda s, *a, **k: s._base_control.AddStaticMarker(*a, **k)
    add_static_text_marker    = AddStaticTextMarker    = lambda s, *a, **k: s._base_control.AddStaticTextMarker(*a, **k)
    remove_entity_marker      = RemoveEntityMarker     = lambda s, *a, **k: s._base_control.RemoveEntityMarker(*a, **k)
    remove_entity_text_marker = RemoveEntityTextMarker = lambda s, *a, **k: s._base_control.RemoveEntityTextMarker(*a, **k)
    remove_static_marker      = RemoveStaticMarker     = lambda s, *a, **k: s._base_control.RemoveStaticMarker(*a, **k)
    remove_static_text_marker = RemoveStaticTextMarker = lambda s, *a, **k: s._base_control.RemoveStaticTextMarker(*a, **k)
    repaint_mini_map          = RepaintMiniMap         = lambda s, *a, **k: s._base_control.RepaintMiniMap(*a, **k)

    # endregion





