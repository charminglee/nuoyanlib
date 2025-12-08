# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


from typing_extensions import Self
from typing import Optional, NoReturn, Literal
from mod.client.ui.controls.labelUIControl import LabelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
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
    _base_control: LabelUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        label_control: LabelUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
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
    def font_scale(self) -> NoReturn: ...
    @font_scale.setter
    def font_scale(self, val: float) -> None: ...
    @property
    def text_shadow(self) -> bool: ...
    @text_shadow.setter
    def text_shadow(self, val: bool) -> None: ...
    @property
    def text_font(self) -> NoReturn: ...
    @text_font.setter
    def text_font(self, val: __TextFont) -> None: ...
    DisableTextShadow = LabelUIControl.DisableTextShadow
    EnableTextShadow = LabelUIControl.EnableTextShadow
    IsTextShadowEnabled = LabelUIControl.IsTextShadowEnabled
    SetText = LabelUIControl.SetText
    GetText = LabelUIControl.GetText
    SetTextColor = LabelUIControl.SetTextColor
    GetTextColor = LabelUIControl.GetTextColor
    SetTextFontSize = LabelUIControl.SetTextFontSize
    SetTextAlignment = LabelUIControl.SetTextAlignment
    GetTextAlignment = LabelUIControl.GetTextAlignment
    SetTextLinePadding = LabelUIControl.SetTextLinePadding
    GetTextLinePadding = LabelUIControl.GetTextLinePadding
