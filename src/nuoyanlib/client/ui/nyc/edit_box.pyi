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


from typing import NoReturn
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from ....core._types._checker import args_type_check
from ....core._types._typing import NyScreenBaseT
from .control import NyControl


class NyEditBox(NyControl[NyScreenBaseT]):
    _base_control: TextEditBoxUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBaseT,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl[NyScreenBaseT]: ...
    __div__ = __truediv__
    @property
    def edit_text(self) -> str: ...
    @edit_text.setter
    def edit_text(self, val: str) -> None: ...
    @property
    def max_length(self) -> NoReturn: ...
    @max_length.setter
    def max_length(self, val: int) -> None: ...
    get_edit_text = GetEditText = TextEditBoxUIControl.GetEditText
    set_edit_text = SetEditText = TextEditBoxUIControl.SetEditText
    set_edit_text_max_length = SetEditTextMaxLength = TextEditBoxUIControl.SetEditTextMaxLength
