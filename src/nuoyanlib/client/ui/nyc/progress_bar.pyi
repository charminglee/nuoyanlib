# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from typing import Optional, NoReturn
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self


class NyProgressBar(NyControl):
    _base_control: ProgressBarUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        progress_bar_control: ProgressBarUIControl,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def progress(self) -> NoReturn: ...
    @progress.setter
    def progress(self, val: float) -> None: ...
    SetValue = ProgressBarUIControl.SetValue
