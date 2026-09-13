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


from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyScrollView",
]


class NyScrollView(NyControl):
    """
    滚动视图控件类。

    示例
    ----

    >>> self.scroll_view = nyl.NyScrollView(self, "/panel/scroll_view")
    >>> self.scroll_view.scroll_pct = 100

    参见
    ----

    - ``NyControl.to_scroll_view()`` -- 将通用控件实例转换为滚动视图控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该滚动视图控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.SCROLL_VIEW

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def scroll_pos(self):
        """
        [可读写属性]

        当前滚动视图最上方内容的位置。

        :rtype: float
        """
        return self._base_control.GetScrollViewPos()

    @scroll_pos.setter
    def scroll_pos(self, val):
        """
        [可读写属性]

        当前滚动视图最上方内容的位置。

        :type val: float
        """
        self._base_control.SetScrollViewPos(val)

    @property
    def scroll_pct(self):
        """
        [可读写属性]

        当前滚动视图内容的百分比位置。

        :rtype: int
        """
        return self._base_control.GetScrollViewPercentValue()

    @scroll_pct.setter
    def scroll_pct(self, val):
        """
        [可读写属性]

        当前滚动视图内容的百分比位置。

        :type val: int
        """
        self._base_control.SetScrollViewPercentValue(val)

    @property
    def scroll_content_path(self):
        """
        [只读属性]

        滚动视图内容控件的路径。

        :rtype: str
        """
        return self._base_control.GetScrollViewContentPath()

    @property
    def scroll_content(self):
        """
        [只读属性]

        滚动视图内容控件的 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl(self.ny_screen_node, self.scroll_content_path)

    # endregion

    # region Compatibility =============================================================================================

    set_scroll_view_pos             = SetScrollViewPos            = lambda s, *a, **k: s._base_control.SetScrollViewPos(*a, **k)
    get_scroll_view_pos             = GetScrollViewPos            = lambda s, *a, **k: s._base_control.GetScrollViewPos(*a, **k)
    set_scroll_view_percent_value   = SetScrollViewPercentValue   = lambda s, *a, **k: s._base_control.SetScrollViewPercentValue(*a, **k)
    get_scroll_view_percent_value   = GetScrollViewPercentValue   = lambda s, *a, **k: s._base_control.GetScrollViewPercentValue(*a, **k)
    get_scroll_view_content_path    = GetScrollViewContentPath    = lambda s, *a, **k: s._base_control.GetScrollViewContentPath(*a, **k)
    get_scroll_view_content_control = GetScrollViewContentControl = lambda s, *a, **k: s._base_control.GetScrollViewContentControl(*a, **k)

    # endregion





