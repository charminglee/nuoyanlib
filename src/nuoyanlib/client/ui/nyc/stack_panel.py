# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyStackPanel",
]


class NyStackPanel(NyControl):
    """
    栈面板控件类。

    示例
    ----

    >>> self.stack_panel = nyl.NyStackPanel(self, "/panel/stack_panel")
    >>> self.stack_panel.orientation = "horizontal"

    参见
    ----

    - ``NyStackPanel.orientation`` -- 获取/设置栈面板排列方向。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该栈面板控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.STACK_PANEL

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def orientation(self):
        """
        [可读写属性]

        栈面板排列方向。

        :rtype: str
        """
        return self._base_control.GetOrientation()

    @orientation.setter
    def orientation(self, val):
        """
        [可读写属性]

        栈面板排列方向。

        :type val: str
        """
        self._base_control.SetOrientation(val)

    # endregion

    # region Compatibility =============================================================================================

    set_orientation = SetOrientation = lambda s, *a, **k: s._base_control.SetOrientation(*a, **k)
    get_orientation = GetOrientation = lambda s, *a, **k: s._base_control.GetOrientation(*a, **k)

    # endregion






