# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


if 0:
    from ..screen_node import ScreenNodeExtension


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyStackPanel",
]


class NyStackPanel(NyControl):
    """
    栈面板控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 栈面板所在UI类的实例（需继承 ScreenNodeExtension）
    :param StackPanelUIControl stack_panel_control: 通过 asStackPanel() 等方式获取的 StackPanelUIControl 实例
    """

    CONTROL_TYPE = ControlType.STACK_PANEL

    def __init__(self, screen_node_ex, stack_panel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, stack_panel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

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











