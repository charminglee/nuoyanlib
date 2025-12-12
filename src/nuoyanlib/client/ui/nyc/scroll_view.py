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
    from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
    from ..screen_node import ScreenNodeExtension


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyScrollView",
]


class NyScrollView(NyControl):
    """
    滚动视图控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 滚动视图所在UI类的实例（需继承ScreenNodeExtension）
    :param ScrollViewUIControl scroll_view_control: 通过asScrollView()等方式获取的ScrollViewUIControl实例
    """

    CONTROL_TYPE = ControlType.SCROLL_VIEW

    def __init__(self, screen_node_ex, scroll_view_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, scroll_view_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def scroll_pos(self):
        """
        [可读写属性]

        当前ScrollView最上方内容的位置。

        :rtype: float
        """
        return self._base_control.GetScrollViewPos()

    @scroll_pos.setter
    def scroll_pos(self, val):
        """
        [可读写属性]

        当前ScrollView最上方内容的位置。

        :type val: float
        """
        self._base_control.SetScrollViewPos(val)

    @property
    def scroll_pct(self):
        """
        [可读写属性]

        当前ScrollView内容的百分比位置。

        :rtype: int
        """
        return self._base_control.GetScrollViewPercentValue()

    @scroll_pct.setter
    def scroll_pct(self, val):
        """
        [可读写属性]

        当前ScrollView内容的百分比位置。

        :type val: int
        """
        self._base_control.SetScrollViewPercentValue(int(val))

    @property
    def scroll_content_path(self):
        """
        [只读属性]

        ScrollView内容控件的路径。

        :rtype: str
        """
        return self._base_control.GetScrollViewContentPath()

    @property
    def scroll_content(self):
        """
        [只读属性]

        ScrollView内容控件的 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.from_path(self.ui_node, self.scroll_content_path)

    # endregion











