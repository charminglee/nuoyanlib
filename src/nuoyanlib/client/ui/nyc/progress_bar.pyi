# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-30
|
| ====================================================
"""


from typing import Optional, NoReturn
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NyProgressBar(NyControl):
    _base_control: ProgressBarUIControl
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        progress_bar_control: ProgressBarUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def progress(self) -> NoReturn: ...
    @progress.setter
    def progress(self, val: float) -> None: ...
    SetValue = ProgressBarUIControl.SetValue
