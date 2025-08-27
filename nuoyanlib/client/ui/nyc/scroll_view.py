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
    "NyScrollView",
]


class NyScrollView(NyControl):
    """
    | 创建 ``NyScrollView`` 滚动视图实例。

    -----

    :param ScreenNodeExtension screen_node_ex: 滚动视图所在UI类的实例（需继承ScreenNodeExtension）
    :param ScrollViewUIControl scroll_view_control: 通过asScrollView()等方式获取的ScrollViewUIControl实例
    """

    _CONTROL_TYPE = ControlType.SCROLL_VIEW

    def __init__(self, screen_node_ex, scroll_view_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, scroll_view_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    @property
    def scroll_pos(self):
        """
        [可读写属性]

        | 当前ScrollView最上方内容的位置。

        :rtype: float
        """
        return self.base_control.GetScrollViewPos()

    @scroll_pos.setter
    def scroll_pos(self, val):
        """
        [可读写属性]

        | 当前ScrollView最上方内容的位置。

        :type val: float
        """
        self.base_control.SetScrollViewPos(val)

    @property
    def scroll_pct(self):
        """
        [可读写属性]

        | 当前ScrollView内容的百分比位置。

        :rtype: int
        """
        return self.base_control.GetScrollViewPercentValue()

    @scroll_pct.setter
    def scroll_pct(self, val):
        """
        [可读写属性]

        | 当前ScrollView内容的百分比位置。

        :type val: int
        """
        self.base_control.SetScrollViewPercentValue(int(val))

    @property
    def content_path(self):
        """
        [只读属性]

        | ScrollView内容控件的路径。

        :rtype: str
        """
        return self.base_control.GetScrollViewContentPath()

    @property
    def content_control(self):
        """
        [只读属性]

        | ScrollView内容控件的 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.from_path(self.ui_node, self.content_path)

    # endregion











