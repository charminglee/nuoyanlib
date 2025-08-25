# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-26
|
| ==============================================
"""


from typing import Optional, NoReturn
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


class NyEditBox(NyControl):
    base_control: TextEditBoxUIControl
    """
    | 文本编辑框 ``TextEditBoxUIControl`` 实例。
    """
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

    def GetEditText(self) -> str:
        """
        | 获取edit_box输入框的文本信息，获取失败会返回 ``None`` 。

        -----

        :return: 输入框的文本信息
        :rtype: str|None
        """
    def SetEditText(self, text: str) -> None:
        """
        | 设置edit_box输入框的文本信息。

        -----

        :param str text: 输入框的文本信息

        :return: 无
        :rtype: None
        """
    def SetEditTextMaxLength(self, max_length: int) -> None:
        """
        | 设置输入框的最大输入长度。

        -----

        :param int max_length: 最大输入长度

        :return: 无
        :rtype: None
        """
