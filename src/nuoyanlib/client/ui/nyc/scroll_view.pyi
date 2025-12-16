# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from typing import Optional
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self


class NyScrollView(NyControl):
    _base_control: ScrollViewUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        scroll_view_control: ScrollViewUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
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
    SetScrollViewPos = ScrollViewUIControl.SetScrollViewPos
    GetScrollViewPos = ScrollViewUIControl.GetScrollViewPos
    SetScrollViewPercentValue = ScrollViewUIControl.SetScrollViewPercentValue
    GetScrollViewPercentValue = ScrollViewUIControl.GetScrollViewPercentValue
    GetScrollViewContentPath = ScrollViewUIControl.GetScrollViewContentPath
    GetScrollViewContentControl = ScrollViewUIControl.GetScrollViewContentControl
