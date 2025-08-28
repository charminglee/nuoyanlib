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
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


class NyProgressBar(NyControl):
    base_control: ProgressBarUIControl
    """
    | 进度条 ``ProgressBarUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        progress_bar_control: ProgressBarUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def value(self) -> NoReturn: ...
    @value.setter
    def value(self, val: float) -> None: ...

    def SetValue(self, progress: float) -> None:
        """
        | 设置进度条的进度。

        -----

        :param float progress: 进度，范围为[0, 1]

        :return: 无
        :rtype: None
        """
