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


from typing import Optional, Literal
from mod.client.ui.controls.labelUIControl import LabelUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check
from ....core._types._typing import FTuple3


__TextFont = Literal[
    "rune",
    "unicode",
    "smooth",
    "default",
]
__TextAlignment = Literal[
    "left",
    "right",
    "center",
]


class NyLabel(NyControl):
    __font_scale: float
    _base_control: LabelUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def text(self) -> Optional[str]: ...
    @text.setter
    def text(self, val: str) -> None: ...
    @property
    def text_alignment(self) -> __TextAlignment: ...
    @text_alignment.setter
    def text_alignment(self, val: __TextAlignment) -> None: ...
    @property
    def text_color(self) -> FTuple3: ...
    @text_color.setter
    def text_color(self, val: FTuple3) -> None: ...
    @property
    def line_padding(self) -> float: ...
    @line_padding.setter
    def line_padding(self, val: float) -> None: ...
    @property
    def font_scale(self) -> float: ...
    @font_scale.setter
    def font_scale(self, val: float) -> None: ...
    @property
    def text_shadow(self) -> bool: ...
    @text_shadow.setter
    def text_shadow(self, val: bool) -> None: ...
    def set_text_font(self, font: __TextFont) -> None: ...
    disable_text_shadow = DisableTextShadow = LabelUIControl.DisableTextShadow
    enable_text_shadow = EnableTextShadow = LabelUIControl.EnableTextShadow
    is_text_shadow_enabled = IsTextShadowEnabled = LabelUIControl.IsTextShadowEnabled
    set_text = SetText = LabelUIControl.SetText
    get_text = GetText = LabelUIControl.GetText
    set_text_color = SetTextColor = LabelUIControl.SetTextColor
    get_text_color = GetTextColor = LabelUIControl.GetTextColor
    set_text_font_size = SetTextFontSize = LabelUIControl.SetTextFontSize
    set_text_alignment = SetTextAlignment = LabelUIControl.SetTextAlignment
    get_text_alignment = GetTextAlignment = LabelUIControl.GetTextAlignment
    set_text_line_padding = SetTextLinePadding = LabelUIControl.SetTextLinePadding
    get_text_line_padding = GetTextLinePadding = LabelUIControl.GetTextLinePadding
