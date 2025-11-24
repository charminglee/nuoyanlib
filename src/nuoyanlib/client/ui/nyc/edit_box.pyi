# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-29
|
| ====================================================
"""


from typing import Optional, NoReturn
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NyEditBox(NyControl):
    _base_control: TextEditBoxUIControl
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        edit_box_control: TextEditBoxUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def edit_text(self) -> str: ...
    @edit_text.setter
    def edit_text(self, val: str) -> None: ...
    @property
    def max_length(self) -> NoReturn: ...
    @max_length.setter
    def max_length(self, val: int) -> None: ...
    GetEditText = TextEditBoxUIControl.GetEditText
    SetEditText = TextEditBoxUIControl.SetEditText
    SetEditTextMaxLength = TextEditBoxUIControl.SetEditTextMaxLength
