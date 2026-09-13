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
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from ....core._types._checker import args_type_check
from ....core._types._typing import NyScreenBaseT
from .control import NyControl


class NyProgressBar(NyControl[NyScreenBaseT]):
    _base_control: ProgressBarUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBaseT,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl[NyScreenBaseT]: ...
    __div__ = __truediv__
    @property
    def progress(self) -> NoReturn: ...
    @progress.setter
    def progress(self, val: float) -> None: ...
    set_value = SetValue = ProgressBarUIControl.SetValue
