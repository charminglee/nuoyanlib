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


from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


class NyScrollView(NyControl):
    _base_control: ScrollViewUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def scroll_pos(self) -> float: ...
    @scroll_pos.setter
    def scroll_pos(self, val: float) -> None: ...
    @property
    def scroll_pct(self) -> int: ...
    @scroll_pct.setter
    def scroll_pct(self, val: int) -> None: ...
    @property
    def scroll_content_path(self) -> str: ...
    @property
    def scroll_content(self) -> NyControl: ...
    set_scroll_view_pos = SetScrollViewPos = ScrollViewUIControl.SetScrollViewPos
    get_scroll_view_pos = GetScrollViewPos = ScrollViewUIControl.GetScrollViewPos
    set_scroll_view_percent_value = SetScrollViewPercentValue = ScrollViewUIControl.SetScrollViewPercentValue
    get_scroll_view_percent_value = GetScrollViewPercentValue = ScrollViewUIControl.GetScrollViewPercentValue
    get_scroll_view_content_path = GetScrollViewContentPath = ScrollViewUIControl.GetScrollViewContentPath
    get_scroll_view_content_control = GetScrollViewContentControl = ScrollViewUIControl.GetScrollViewContentControl
